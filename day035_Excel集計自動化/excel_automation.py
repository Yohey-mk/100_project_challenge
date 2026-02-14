# excel_automation.py

import pandas as pd
import random

# 1. Dummny Dataを作成(後にエクセルを読み込むGUIボタンなどを作成)
print("1. ダミーデータを作成中...")

brands = ["NIKE", "Adidas", "Asics", "New Balance", "ON", "HOKA"]
categories = ["Shoes", "Apparel", "Accessery", "Other"]
apparel_products = ["Tops", "Bottoms", "Jacket", "Outer", "Other"]
accessery_products = ["Bags", "Socks", "Caps", "Other"]
# shoesのカタログ辞書を作り、後半のelif brand...の部分でDRY原則を守れるようにする
#nike_products = ["Air Force1", "Air Jordan 1", "AIR MAX90", "DUNK", "SHOX", "Cortez", "Vomero"]
#adidas_products = ["Samba", "Gazelle", "Tobacco", "Spezial", "Stan Smith"]
#asics_products = ["Metaspeed", "Gel-Kayano", "Gel-Nunobiki", "Gel-Nimbus", "Gel-NYC"]
#nb_products = ["1906L", "USA 990", "2002R", "574 Core", "CM996", "530"]
#on_products = ["Cloud 6", "Cloudtilt", "The Roger", "Cloudsurfer", "Cloudrock", "Cloudmonster"]
#hoka_products = ["Clifton 10", "Bondi 9", "Stealth/Tech", "Transport 2", "Mafate", "Hopara"]
shoe_catalog = {
    "NIKE": {"Air Force1": 16500, "Air Jordan 1": 16500, "AIR MAX90": 16500, "DUNK": 15400, "SHOX": 26730, "Cortez": 12430, "Vomero": 22330},
    "Adidas": {"Samba": 15950, "Gazelle": 15400, "Tobacco": 15400, "Spezial": 16500, "Stan Smith": 13200},
    "Asics": {"Metaspeed": 29700, "Gel-Kayano": 28600, "Gel-Nunobiki": 15400, "Gel-Nimbus": 20900, "Gel-NYC": 18700},
    "New Balance": {"1906L": 22000, "USA 990": 39600, "2002R": 19800, "574 Core": 13970, "CM996": 16940, "530": 12980},
    "ON": {"Cloud 6":18700, "Cloudtilt": 23100, "The Roger": 25300, "Cloudsurfer":24200, "Cloudrock":24200, "Cloudmonster": 24200},
    "HOKA": {"Clifton 10": 19800, "Bondi 9": 24200, "Stealth/Tech": 24200, "Transport 2": 22000, "Mafate": 29700, "Hopara": 18150}
}

data = []

for i in range(100):
    date = f"2026-01-{random.randint(1, 31):02d}"
    brand = random.choice(brands)
    category = random.choice(categories)
    product = ""
    price = 0

    if category == "Apparel":
        product = random.choice(apparel_products)
        price = random.randint(5000, 20000)
    elif category == "Accessery":
        product = random.choice(accessery_products)
        price = random.randint(1000, 15000)
    elif category == "Other":
        product = "Other"
        price = random.randint(500, 5000)
    elif category == "Shoes": # shoe_catalogの辞書から取り出すようにして、以下の長いif分岐を削除する
        if brand in shoe_catalog:
            brand_items = shoe_catalog[brand]
            # キーのリストからランダムに１つ選ぶ
            product = random.choice(list(brand_items.keys()))
            # 選ばれたキーを使って、値段を取り出す
            price = brand_items[product]
        else:
            product = "Unknown"
            price = 10000
    #if brand == "NIKE" and category == "Shoes":
    #    product = random.choice(nike_products)
    #elif brand == "Adidas" and category == "Shoes":
    #    product = random.choice(adidas_products)
    #elif brand == "Asics" and category == "Shoes":
    #    product = random.choice(asics_products)
    #elif brand == "New Balance" and category == "Shoes":
    #    product = random.choice(nb_products)
    #elif brand == "ON" and category == "Shoes":
    #    product = random.choice(on_products)
    #elif brand == "HOKA" and category == "Shoes":
    #    product = random.choice(hoka_products)
    quantity = random.randint(1, 3)
    data.append([date, brand, category, product, price, quantity])

# CSVに保存
df_original = pd.DataFrame(data, columns=['date', 'brand', 'category', 'product', 'price', 'quantity'])
df_original.to_csv("sales_raw.csv", index=False, encoding="utf-8-sig")

print("'sales_raw.csv'を作成しました。")

# 2. データの読み込みと集計
df = pd.read_csv("sales_raw.csv")
df["total_sales"] = df["price"] * df["quantity"]

# 商品ごとにグループ化して売上金額を合計する
summary_df = df.groupby(["brand", "product"])[["quantity", "total_sales"]].sum()

# 売上が高い順に並び替え
summary_df = summary_df.sort_values("total_sales", ascending=False)
print(" --- 集計完了 --- ")
print(summary_df)

# 3. Excelファイルへ書き出す
print("Exporting as Excel file...")

output_file = "sales_report.xlsx"

# ExcelWriteを使い、１つのファイルに複数のシートを作る
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    # sheet1: summary
    summary_df.to_excel(writer, sheet_name="商品別集計")

    # sheet2: 元データ
    df.to_excel(writer, sheet_name="raw_data", index=False)

print(f"{output_file}に保存しました。")