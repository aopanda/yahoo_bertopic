# -*- coding: utf-8 -*-

"""
2023年8月時点ではスクレイピング可能でした。

こちらのコードを参考に作りました：
https://gist.github.com/jshirius/e8992c0e7620de098a43d77e4bd91859

プロジェクト全体の説明は以下リンクを参照ください：
https://note.com/ati_sum/n/n236c2669b6dd
このファイルのコードは「2-1. スクレイピングでデータ取得」部分です。
検索結果を関連度順にデータ抽出したい場合は、"yahoo_scraping_default.py"ファイルを使用してください。

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
# 特定のURLでブラウザを起動する
driver.get("https://www.google.com/?hl=ja")
time.sleep(3)

# driver.find_elements_by_css_selector("xxx") 的な処理を自由に
print("サイトのタイトル：", driver.title)
print("\nお疲れさまです。\n処理が完了しました。")

url = "<url>"
def get_post(url):
    # xpath2 = '//*[@id="que"]/div/div/div[2]/div/div/div[2]/div/p'
    class_name = 'ClapLv1TextBlock_Chie-TextBlock__3X4V5'
    driver.get(url)
    elements = driver.find_elements(by=By.CLASS_NAME, value=class_name)

    texts = []
    for element in elements[:1]:
        texts.append(element.text)
    return texts

def next_page_action():
    """
    現在のページから次のページを読み込むアクションを実行する
    """
    rtn = False

    # 次へボタンのクリック
    elems = driver.find_elements(By.XPATH, '//*[@id="pg_low"]/div/a[*]')
    # 現在のページ
    print("ページ遷移前のurl:")
    print(driver.current_url)
    if (len(elems) == 0):
        print("次のページは存在しないよ〜")
    else:
        for elem in elems:
            # print(elem.text)
            if (elem.text != "次へ"):
                continue
            url = elem.get_attribute('href')
            driver.get(url)
            rtn = True
            break

    return rtn

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import pandas as pd


PAGE_LIMIT = 100
KEYWORDS = ['子育て', '育児', '子育て　悩み', '育児　悩み']
SQRAPING_URL = "https://chiebukuro.yahoo.co.jp/"

# Setting the driver
# Provide the path to your chromedriver executable
path_to_chromedriver = './chromedriver'

# Provide the absolute path to the Chrome binary
path_to_chrome_binary = '/usr/bin/google-chrome'

# Create a Service object
service = Service()
options = webdriver.ChromeOptions()

# Set the Chrome binary location
options = Options()
options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument('--window-size=1920,1080')

# Pass the Service object and options to the webdriver.Chrome() method
driver = webdriver.Chrome(service=service, options=options)

# Load the webpage
driver.get(SQRAPING_URL)
# 思っているサイトにアクセスできているかチェックする場合は下記のsave_screenshotを使います。
# driver.save_screenshot("test.png")
print("website accessed successfully")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep


for keyword in KEYWORDS:
    print(keyword)
    driver.get(SQRAPING_URL)
    xpath999 = '//*[@id="Top"]/div/div[1]/div[2]/nav/div[1]/div/div/div/input'
    search_boxes = driver.find_elements(by=By.XPATH, value=xpath999)

    if len(search_boxes) > 0:
        # Select the first element from the list
        search_box = search_boxes[0]

        # Use the send_keys() method on the selected element
        search_box.send_keys(keyword)

        # Find the search button container
        search_button_container = driver.find_elements(By.CLASS_NAME, "SearchBox_searchBox__wrap__2zBaE")

        # Check if any elements were found
        if len(search_button_container) > 0:
            # Select the first element from the list
            search_button = search_button_container[0].find_element(By.CLASS_NAME, 'cl-noclick-log.SearchBox_searchBox__inputButton__2OXXW')

            # Click the search button
            search_button.click()
            sleep(2)

            sort = Select(driver.find_element(By.XPATH, '//*[@id="SearchResults"]/div/div[2]/div[2]/div[2]/div/div/label/select'))
            # ソートするフィルターのタイプによって指定する番号が以下のように変わります。他のフィルタータイプはサイトのソースコードでご確認ください。
            # 20 = sort by newer post dates, 6 = sort by # of views
            sort.select_by_value('20')
            sleep(2)
            driver.save_screenshot(keyword + ".png")

        else:
            print("No search button container found.")
    else:
        print("No search boxes found.")

    analysis_list = []
    text_list = []

    for page in range(PAGE_LIMIT):
        print("ページ %dを実行中" % page)
        sleep(5)

        # 次のページに遷移する
        rtn = next_page_action()
        if rtn == False or page >= PAGE_LIMIT:
            break

        xpath1 = "//li/h3/a"
        elems = driver.find_elements(by=By.XPATH, value=xpath1)

        # 取得した要素を1つずつ表示
        out_puts = []

        if (len(elems) == 0):
            print("ページは存在しないよ〜")
        else:
            for i, elem in enumerate(elems):
                out_dic = {}
                out_dic['query_key'] = keyword
                url = elem.get_attribute('href')
                out_dic['rs_link'] = url
                out_dic['summary'] = elem.text

                xpath5 = f'#sr > ul > li:nth-child({i + 1}) > p.ListSearchResults_listSearchResults__information__3uanU > span.ListSearchResults_listSearchResults__informationDate__10t00 > span:nth-child(3)'
                date = driver.find_element(by=By.CSS_SELECTOR, value=xpath5)
                out_dic['post_date'] = date.text

                out_puts.append(out_dic)

            if len(out_puts) > 0:
                analysis_list.extend(out_puts)
                df = pd.DataFrame(analysis_list)


    for link in df['rs_link']:
        text_list += get_post(link)
        df['text'] = pd.DataFrame(text_list)

    #ソートのタイプによってcsv_file_nameを変更してください。
    csv_file_name = "Sort_by_latest_post" + keyword + ".csv"
    #csv_file_name = keyword + "_sorted_by_views"+".csv"

    df.to_csv(csv_file_name, encoding="utf_8_sig")

driver.close()
driver.quit()