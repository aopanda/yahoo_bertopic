import pandas as pd
from plotly.offline import iplot

#pd.set_option('display.max_columns', None)

# Reading csv data into dataframes again
# Change file names accordingly / as necessary
df1 = pd.read_csv("子育て.csv", encoding='utf_8')
df2 = pd.read_csv("育児.csv", encoding='utf_8')
df3 = pd.read_csv("子育て　悩み.csv", encoding='utf_8')
df4 = pd.read_csv("育児　悩み.csv", encoding='utf_8')
df5 = pd.read_csv("Sort_by_latest_post育児　悩み.csv", encoding='utf_8')
df6 = pd.read_csv("育児　悩み_sorted_by_views.csv", encoding='utf_8')
df7 = pd.read_csv("Sort_by_latest_post育児.csv", encoding = 'utf_8')
df8 = pd.read_csv("育児_sorted_by_views.csv", encoding = 'utf_8')
df9 = pd.read_csv("Sort_by_latest_post子育て　悩み.csv", encoding = 'utf_8')
df10 = pd.read_csv("子育て　悩み_sorted_by_views.csv", encoding = 'utf_8')
df11 = pd.read_csv("Sort_by_latest_post子育て.csv", encoding = 'utf_8')
df12 = pd.read_csv("子育て_sorted_by_views.csv", encoding = 'utf_8')

#print(df1.shape)
#print(df1.head(5))

frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]
df_all = pd.concat(frames, ignore_index=True)
print("df_all shape - pre cleaning duplicates" + str(df_all.shape))

# ---------
# Removing duplicated posts
print("rs_link duplicates\n" + str(df_all.duplicated('rs_link').value_counts()))
print("summary duplicates\n" + str(df_all.duplicated('summary').value_counts()))

print("duplicated text")
print("text duplicates\n" + str(df_all.duplicated('text').value_counts()))

df_all['duplicate_rs_link'] = df_all['rs_link'].duplicated()
df_all['duplicate_summary'] = df_all['summary'].duplicated()
df_all['duplicate_text'] = df_all['text'].duplicated()

df_all.drop_duplicates(subset='text', keep='first', inplace=True)

df_all.reset_index(inplace=True)
print(df_all.head(10))
print(df_all.tail(10))
print("df_all shape post cleaning duplicates \n" + str(df_all.shape))

# ---------


# --------
# Converting datetime to date
#print(df_all['post_date'].head(10))
df_all['post_date'] = pd.to_datetime(df_all['post_date'])

# Extract year each post was posted
df_all['post_year'] = df_all['post_date'].dt.year
print(df_all['post_date'].dtype)
df_all = df_all.sort_values(by=['post_date'])
print(df_all['post_date'].head(10))
# ---------

# --------
# cleaning texts and characters

print("Checking https in text")
print(df_all['text'].str.contains('http').sum())

import re
import neologdn
#import unidic

def cleaning_post(text):
    #全角・半角の統一と重ね表現の除去
    normalized_text = neologdn.normalize(text)
    #normalized_text = unidic.normalize(text)
    #URLや記号の削除、数字の置換
    text_without_url = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', normalized_text)

    #ここで「」はスペース開かないようにする？考え中
    code_regex = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')
    text_without_url = code_regex.sub(' ', text_without_url)

    tmp = re.sub(r'(\d)([,.])(\d+)', r'\1\3',  text_without_url)
    #text_replaced_number = re.sub("\d", "0", tmp)
    #text_replaced_number = text_replaced_number.replace("\n", ' ').replace('\r',' ')
    #return text_replaced_number

    text_replaced = tmp.replace("\n", ' ').replace('\r', ' ')
    return text_replaced

#df_all['summary_clean'] = df_all['summary'].apply(cleaning_post)
df_all['text_clean'] = df_all['text'].apply(cleaning_post)

df_all['summary_wakati'] = df_all['summary'].apply(cleaning_post)
df_all['text_wakati'] = df_all['text'].apply(cleaning_post)

#print(df_all.head(10))
print("Sum of any text cells with https\n" + str(df_all['text_wakati'].str.contains('http').sum()))

#print(df_all['text_clean'].dtype)
df_all['text_clean_split'] = df_all['text_wakati'].str.split()

# --------
# 形態素解析
# --------

import MeCab

def sep_by_mecab(text):
    #unidic
    #m = MeCab.Tagger('-Owakati')
    # ---- neoloagd
    m = MeCab.Tagger ("-d/opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd")

    node = m.parseToNode(text)

    word_list=[]
    while node:
        hinshi = node.feature.split(",")[0]
        #名詞、動詞、形容詞のみを抽出する
        if hinshi in ["名詞","動詞","形容詞","固有名詞"]:
        #if hinshi in ["名詞", "動詞", "形容詞"]:
            origin = node.feature.split(",")[6]
            #抽出したくない単語を、stopwprdとして設定する
            if origin not in ["*","する","いる","なる","てる","れる","ある","こと","もの"] :
                word_list.append(origin)
        node = node.next

    return word_list


#df_all['summary_wakati'] = df_all['summary_clean'].apply(sep_by_mecab)
#df_all['text_wakati'] = df_all['text_clean'].apply(sep_by_mecab)
df_all['summary_wakati'] = df_all['summary_wakati'].apply(sep_by_mecab)
df_all['text_wakati'] = df_all['text_wakati'].apply(sep_by_mecab)

#print(df_all.head(10))
#print(df_all.tail(10))

print(df_all.shape)


df_all.to_csv("all_parenting_concern_posts.csv", encoding="utf_8")

df_2023 = df_all.query('post_year == 2023').reset_index()
print(df_2023.shape)
df_2023.to_csv("2023_parenting_concern_posts.csv", encoding="utf_8")


# ---------
# Visualize distribution of posts over the years
import numpy as np

import matplotlib.pyplot as plt

x = df_all['post_year'].unique().tolist()
y = df_all.groupby('post_year')['post_year'].count()
print(y)

plt.bar(x, y, width=0.8, bottom=None, data=None, tick_label=x)
plt.title('Number of extracted posts per year')
plt.show()

# ---------

# ---------
# Get average length of posts
print("Average length of posts")

df_all["text_counts"] = df_all["text"].apply(lambda x: len(x))
#print(df_all['text_counts'].median())
print(df_all['text_counts'].mean())


# -------



# --------
# nlplot

import nlplot
from plotly.offline import iplot
import matplotlib.pyplot as plt

npt = nlplot.NLPlot(df_all, target_col='text_wakati')
#npt = nlplot.NLPlot(df_2023, target_col='text_wakati')
stopwords = ["の","ん","ない","てる","一","これ","私","ところ","ため","思う","やる","せる","くれる","よう","みる","さん","そう","くださる"]
#NOTE - find top words to remove from a website I saw...

# ビルド（データ件数によっては処理に時間を要します）
npt.build_graph(stopwords=stopwords,
                min_edge_frequency=750)


# ビルド後にノードとエッジの数が表示される。ノードの数が100前後になるようにするとネットワークが綺麗に描画できる
fig_co_network = npt.co_network(
    title='Co-occurrence network',
    sizing=100,
    node_size='adjacency_frequency',
    color_palette='hls',
    width=1100,
    height=700,
    save=False
)
iplot(fig_co_network)

fig_tm = npt.treemap(
    title='Tree of Most Common Words',
    ngram=1,
    top_n=30,
    stopwords=stopwords,
)
iplot(fig_tm)

fig_wc = npt.wordcloud(
    width=1000,
    height=600,
    max_words=100,
    max_font_size=100,
    colormap='tab20_r',
    #colormap='tab10_r',
    stopwords=stopwords,
    mask_file=None,
    save=False
)
plt.figure(figsize=(8.0, 6.0))
plt.imshow(fig_wc, interpolation="bilinear")
plt.axis("off")
plt.show()


'''

fig_unigram = npt.bar_ngram(
    title='uni-gram',
    xaxis_label='word_count',
    yaxis_label='word',
    ngram=1,
    top_n=50,
    width=800,
    height=1100,
    color=None,
    horizon=True,
    stopwords=stopwords,
    verbose=False,
    save=False,
)
fig_unigram.show()
'''

'''
fig_wc = npt.wordcloud(
    width=1000,
    height=600,
    max_words=100,
    max_font_size=100,
    colormap='tab20_r',
    stopwords=stopwords,
    mask_file=None,
    save=False
)
plt.figure(figsize=(8.0, 6.0))
plt.imshow(fig_wc, interpolation="bilinear")
plt.axis("off")
plt.show()
'''
