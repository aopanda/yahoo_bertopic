# -*- coding: utf-8 -*-

"""
2023年8月時点ではスクレイピング可能でした。

こちらのコードを参考に作りました：
https://gist.github.com/jshirius/e8992c0e7620de098a43d77e4bd91859

プロジェクト全体の説明は以下リンクを参照ください：
https://note.com/ati_sum/n/n236c2669b6dd
このファイルのコードは「2-1. スクレイピングでデータ取得」部分です。
関連順に表示されたキーワード検索の結果を抽出しています。
検索後に結果をソートしてから(投稿日が新しい順・閲覧数が多い順など）データ抽出したい場合は、"yahoo_scraping_sorting.py"ファイルを使用してください。

実装環境：
MacBook Air (M1)で、PyCharmまたはGoogle Colaboratory上でPython3を使用しました。
"""

# まずはSeleniumからwebdriverをインポートし、ブラウザを起動していきます。

# こちらのコードはPyCharmでローカル環境で実装したので、事前にSeleniumを別途インストールしました。
# ご自身の環境等に合わせて、!pip install seleniumなどでSeleniumをインストールしてください。

# Google Chromeも事前にインストール済み

# ---------------------------------------------------------------------------------------
# ブラウザ起動に使うライブラリをインポート
# ---------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import time
from time import sleep

# ---------------------------------------------------------------------------------------
# 処理開始
# ---------------------------------------------------------------------------------------
# ブラウザをheadlessモード実行
print("\nブラウザを設定")

service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)


# サイトにアクセス
print("サイトにアクセス開始")
# 特定のURLでブラウザを起動する - Google Japanサイト
driver.get("https://www.google.com/?hl=ja")
time.sleep(3)

# サイトのタイトルでGoogleが起動されているか確認
print("サイトのタイトル：", driver.title)
print("\nお疲れさまです。\n処理が完了しました。")

# -----------------------------------------------------------------
# 関数の設定
# -----------------------------------------------------------------

def analysis_action():
    # まず検索結果ページに出てくる投稿リンクを取得
    xpath1 = "//li/h3/a"
    elems = driver.find_elements(by=By.XPATH, value=xpath1)

    # 取得した要素を1つずつ表示
    out_puts = []

    if (len(elems) == 0):
        # 検索結果ページからリンクがうまく取れていない場合はエラー分を出力（デバグ用）
        print("ページは存在しないよ〜")
    else:
        # 検索結果ページからリンクが取得できていたら各情報をout_dicに格納していく
        for i, elem in enumerate(elems):
            out_dic = {}
            # 使用キーワードを格納
            out_dic['query_key'] = keyword

            # 投稿ポストのURLを格納
            url = elem.get_attribute('href')
            out_dic['rs_link'] = url

            # 投稿ポストの見出しを格納
            out_dic['summary'] = elem.text

            # 投稿ポストの日時をCSS_SELECTORで見つけて格納
            css_date = f'#sr > ul > li:nth-child({i + 1}) > p.ListSearchResults_listSearchResults__information__3uanU > span.ListSearchResults_listSearchResults__informationDate__10t00 > span:nth-child(3)'
            date = driver.find_element(by=By.CSS_SELECTOR, value=css_date)
            out_dic['post_date'] = date.text

            out_puts.append(out_dic)

        return out_puts

# -----------------------------------------------------------------

def get_post(url):
    class_name = 'ClapLv1TextBlock_Chie-TextBlock__3X4V5'
    driver.get(url)
    elements = driver.find_elements(by=By.CLASS_NAME, value=class_name)

    texts = []
    for element in elements[:1]:
        texts.append(element.text)
    return texts

# -----------------------------------------------------------------

def next_page_action():
    # 現在のページから次のページを読み込むアクションを実行する
    rtn = False
    # 次へボタンのクリック
    elems = driver.find_elements(By.XPATH, '//*[@id="pg_low"]/div/a[*]')
    # 現在のページを出力
    print("ページ遷移前のurl:")
    print(driver.current_url)
    # 次のページがない場合にメッセージを出力（デバグ用）
    if (len(elems) == 0):
        print("次のページは存在しないよ〜")
    else:
        for elem in elems:
            if (elem.text != "次へ"):
                continue
            url = elem.get_attribute('href')
            driver.get(url)
            rtn = True
            break

    return rtn

# -----------------------------------------------------------------　

# -----------------------------------------------------------------
# スクレイピングの実行
# -----------------------------------------------------------------

# さらに必要なライブラリのインポート
from selenium.webdriver.common.by import By
import pandas as pd


# -----------------------------------------------------------------
# スクレイピングするサイトのURL、使用キーワード、検索するページ数を指定
SQRAPING_URL = "https://chiebukuro.yahoo.co.jp/"
PAGE_LIMIT = 100
KEYWORDS = ['子育て', '育児', '子育て　悩み', '育児　悩み']

# !curl ipinfo.io

for keyword in KEYWORDS:
    # キーワードを出力
    print(keyword)
    # 指定URLにアクセス
    driver.get(SQRAPING_URL)
    print("website accessed successfully")

    # 取得したい要素のXPathを設定、要素を取得
    # 検索ボックスのXpath
    xpath999 = '//*[@id="Top"]/div/div[1]/div[2]/nav/div[1]/div/div/div/input'
    search_boxes = driver.find_elements(by=By.XPATH, value=xpath999)

    if len(search_boxes) > 0:
        search_box = search_boxes[0]
        # キーワードを入れて検索
        search_box.send_keys(keyword)
        # 検索ボタンが入っている入れ物を探す
        search_button_container = driver.find_elements(By.CLASS_NAME, "SearchBox_searchBox__wrap__2zBaE")

        # 検索ボタンが入っている箇所を見つかったら、そこから検索ボタンを取得してクリックする
        if len(search_button_container) > 0:
            search_button = search_button_container[0].find_element(By.CLASS_NAME, 'cl-noclick-log.SearchBox_searchBox__inputButton__2OXXW')
            search_button.click()
            sleep(2)
            # 想定しているページで想定したキーワードで検索できているかを、スクショでチェック
            driver.save_screenshot(keyword + "screenshot.png")
        else:
            # 検索ボタンが見つからない時は下記メッセージを出力（デバグ用）
            print("No search button container found.")
    else:
        # 検索ボックスが見つからない時は下記メッセージを出力（デバグ用）
        print("No search boxes found.")

    # 検索結果が表示されたら、検索結果の各ページから要素を取得。
    # 取得した要素をpandasに格納してcsvに書き出す
    d = analysis_action()
    analysis_list = []
    text_list = []

    # 前述したページ数の数だけ次のページに進んでいく
    for page in range(PAGE_LIMIT):
        print("ページ %dを実行中" % page)
        sleep(5)

        # 次のページに遷移する
        rtn = next_page_action()
        if rtn == False or page >= PAGE_LIMIT:
            break

        # 知恵袋の質問リストを格納する
        if len(d) > 0:
            analysis_list.extend(d)
            df = pd.DataFrame(analysis_list)

    # for page...で取得したリンクにひとつひとつアクセスして、投稿文を取得。
    # 同じデータフレームに格納していく
    for link in df['rs_link']:
        text_list += get_post(link)
        df['text'] = pd.DataFrame(text_list)

    # キーワードごとにcsvに出力していく
    csv_file_name = keyword + ".csv"
    df.to_csv(csv_file_name, encoding="utf_8_sig")

driver.close()
driver.quit()

