# fukuoka_map.py

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium # foliumで作成した地図をStreamlitで表示するための専用ライブラリ

st.set_page_config(page_title="Interactive Map", layout="wide")
st.title("🗺️ インタラクティブ・マップ in 福岡")
st.markdown("Foliumを使って、自由に動かせる地図をアプリに埋め込みます！")

# 1. 地図に表示するデータの準備
# データフレームからピン（マーカー）を立てる準備
def flag_pin(df, m):
    for index, row in df.iterrows():
        folium.Marker(
            location=[row["緯度"], row["経度"]],
            popup=row["スポット名"],
            tooltip="ここをクリック！",
            icon=folium.Icon(color=row["色"])
        ).add_to(m)

# DRYにするためにデータを辞書の辞書にまとめる
area_data ={
    "北九州": {
        "location": [33.8844, 130.8743],
        "data": {
            "スポット名": ["小倉城", "門司港レトロ", "河内藤園", "関門海峡"],
            "緯度": [33.8844, 33.9485, 33.8312, 33.9471],
            "経度": [130.8743, 130.9641, 130.7927, 130.9454],
            "色": ["blue", "red", "green", "purple"]
        }
    },
    "福岡市": {
        "location": [33.5859, 130.3764],
        "data": {
            "スポット名": ["天神駅", "福岡タワー", "大濠公園", "太宰府天満宮"],
            "緯度": [33.5902, 33.5933, 33.5859, 33.5215],
            "経度": [130.4017, 130.3515, 130.3764, 130.5290],
            "色": ["blue", "red", "green", "purple"]
        }
    }
}

area = ["北九州", "福岡市"]
display_option = st.selectbox(label="表示するエリア", options=area)
selected_info = area_data[display_option]
df = pd.DataFrame(selected_info["data"])
m = folium.Map(location=selected_info["location"], zoom_start=12)
flag_pin(df, m)

#if display_option == "北九州":
#    data = {
#        "スポット名": ["小倉城", "門司港レトロ", "河内藤園", "関門海峡"],
#        "緯度": [33.8844, 33.9485, 33.8312, 33.9471],
#        "経度": [130.8743, 130.9641, 130.7927, 130.9454],
#        "色": ["blue", "red", "green", "purple"]
#    }
#    df = pd.DataFrame(data)
#    # 2. 地図のベースを作成
#    m = folium.Map(location=[33.8844, 130.8743], zoom_start=12)
#    flag_pin(df)
#elif display_option == "福岡市":
#    data = {
#        "スポット名": ["天神駅", "福岡タワー", "大濠公園", "太宰府天満宮"],
#        "緯度": [33.5902, 33.5933, 33.5859, 33.5215],
#        "経度": [130.4017, 130.3515, 130.3764, 130.5290],
#        "色": ["blue", "red", "green", "purple"]
#        }
#    df = pd.DataFrame(data)
#    # 2. 地図のベースを作成
#    m = folium.Map(location=[33.5859, 130.3764], zoom_start=12)
#    flag_pin(df)

# 4. Streamlitに地図を描画
st_data = st_folium(m, width=800, height=500)

# 5. クリック検知
st.markdown("---")
st.subheader("👆 クリックされたピンの情報")
# 地図上のピンがクリックされると、その情報がst_dataに返ってきます
if st_data["last_object_clicked"]:
    lat = st_data['last_object_clicked']['lat']
    lng = st_data['last_object_clicked']['lng']
    st.success(f"ピンがクリックされました！座標: (緯度: {lat}, 経度: {lng})")
else:
    st.info("地図上のピンをクリックしてみてください。")