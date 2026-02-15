# excel_automation.py

import pandas as pd
import random

# 1. Dummny Dataを作成(後にエクセルを読み込むGUIボタンなどを作成)
print("1. ダミーデータを作成中...")

brands = ["NIKE", "Adidas", "Asics", "New Balance", "ON", "HOKA"]
categories = ["Shoes", "Apparel", "Accessory", "Other"]
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
    "NIKE": {
        "Air Force1": {"price": 16500, "color": "White"},
        "Air Jordan 1": {"price": 16500, "color": "Black"},
        "AIR MAX90": {"price": 16500, "color": "Grey"},
        "DUNK": {"price": 15400, "color": "Black/White"},
        "SHOX": {"price": 26730, "color": "Silver"},
        "Cortez": {"price": 12430, "color": "White/Red/Blue"},
        "Vomero": {"price": 22330, "color": "Brown"}
        },
    "Adidas": {
        "Samba": {"price": 15950, "color": "White"},
        "Gazelle": {"price": 15400, "color": "Black"},
        "Tobacco": {"price": 15400, "color": "Grey"},
        "Spezial": {"price": 16500, "color": "Black/White"},
        "Stan Smith": {"price": 13200, "color": "Silver"}
        },
    "Asics": {
        "Metaspeed": {"price": 29700, "color": "White"},
        "Gel-Kayano": {"price": 28600, "color": "Black"},
        "Gel-Nunobiki": {"price": 15400, "color": "Grey"},
        "Gel-Nimbus": {"price": 20900, "color": "Black/White"},
        "Gel-NYC": {"price": 18700, "color": "Silver"}
        },
    "New Balance": {
        "1906L": {"price": 22000, "color": "White"},
        "USA 990": {"price": 39600, "color": "Black"},
        "2002R": {"price": 19800, "color": "Grey"},
        "574 Core": {"price": 13970, "color": "Black/White"},
        "CM996": {"price": 16940, "color": "Silver"},
        "530": {"price": 12980, "color": "White/Red"}
        },
    "ON": {
        "Cloud 6": {"price": 18700, "color": "White"},
        "Cloudtilt": {"price": 23100, "color": "Black"},
        "The Roger": {"price": 25300, "color": "Grey"},
        "Cloudsurfer": {"price": 24200, "color": "Black/White"},
        "Cloudrock": {"price": 24200, "color": "Silver"},
        "Cloudmonster": {"price": 24200, "color": "Black/Red"}
        },
    "HOKA": {
        "Clifton 10": {"price": 19800, "color": "Hoka Blue"},
        "Bondi 9": {"price": 24200, "color": "Black"},
        "Stealth/Tech": {"price": 24200, "color": "Grey"},
        "Transport 2": {"price": 22000, "color": "Black/White"},
        "Mafate": {"price": 29700, "color": "Silver"},
        "Hopara": {"price": 18150, "color": "Red/Yellow"}
        }
}

color_catalog = ["Black", "White", "Grey", "Blue", "Red"]

data = []

for i in range(100):
    date = f"2026-01-{random.randint(1, 31):02d}"
    brand = random.choice(brands)
    category = random.choice(categories)
    product = ""
    price = 0
    color = ""

    if category == "Apparel":
        product = random.choice(apparel_products)
        price = random.randint(5000, 20000)
        color = random.choice(color_catalog)
    elif category == "Accessory":
        product = random.choice(accessery_products)
        price = random.randint(1000, 15000)
        color = random.choice(color_catalog)
    elif category == "Other":
        product = "Other"
        price = random.randint(500, 5000)
        color = random.choice(color_catalog)
    elif category == "Shoes": # shoe_catalogの辞書から取り出すようにして、以下の長いif分岐を削除する
        if brand in shoe_catalog:
            brand_items = shoe_catalog[brand]
            # キーのリストからランダムに１つ選ぶ
            product = random.choice(list(brand_items.keys()))
            # productのinfoをすべて取得する
            item_info = shoe_catalog[brand][product]
            # 選ばれたキーを使って、値段を取り出す
            price = item_info["price"]
            color = item_info["color"]
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
    data.append([date, brand, category, product, price, color, quantity])

# CSVに保存
df_original = pd.DataFrame(data, columns=['date', 'brand', 'category', 'product', 'price', 'color', 'quantity'])
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