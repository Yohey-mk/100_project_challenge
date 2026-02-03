# day033_webscraping_app.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. データを取得したいURL
url = "https://news.yahoo.co.jp/topics/top-picks"

# 2. Requestsを使ってWebサイトの情報を取得する
print("Accessing to the website...")
for page_num in range(1, 3):
    url = f"https://news.yahoo.co.jp/topics/top-picks?page={page_num}"
    response = requests.get(url)
    time.sleep(1) # サーバーを攻撃しないように1秒寝る

# 接続に成功したか確認(200ならOK)
if response.status_code == 200:
    print("Success! Start analyzing...")
else:
    print("Failed to access.")
    exit()

# 3. BeautifulSoupを使ってHTMLを解析できる状態にする
soup = BeautifulSoup(response.text, "html.parser")

# 4. データを抽出する
# Yahoo NewsのHTML構造→記事のタイトルは<div class="titleline">の中にあることが分かる
# (サイトのデザイン変更でクラス名が変わることがある)
# ⭐️記事タイトルのクラス名を調べてみる
#target_class = "newsFeed" *classだとUIDが割り当てられており信頼度が低いのでaタグを探す方向にする
#stories = soup.find_all("div", class_=target_class)

data_list = []

all_links = soup.find_all("a")

print(f"全リンク数{len(all_links)}件をチェック中...")

for link_tag in all_links:
    # リンクのURLを取得
    href = link_tag.get("href")

    if href and "pickup" in href:
        title = link_tag.text # aタグの中のテキスト（タイトル）
        if title.strip():
            print(f"Title: {title}")
            print(f"Link: {href}")
            print("-" * 30)

            #  リストに辞書として追加
            data_list.append({"Title": title, "Link": href})

# 5. 重複を削除する & CSVに保存する
if data_list:
    df = pd.DataFrame(data_list)
    df = df.drop_duplicates(subset=["Title"])
    df.to_csv("yahoo_news_list.csv", index=False, encoding="utf-8-sig")
    print(f"\n'yahoo_news_list.csv'に{len(df)}件の記事を保存しました！")
else:
    print("No articles found.")