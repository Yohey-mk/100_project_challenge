# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ページの設定
st.set_page_config(page_title="売上分析ダッシュボード", layout="wide")

# 2. タイトルと説明
st.title("Sales Dashboard")
st.markdown('PythonとStreamlitで作成したインタラクティブ売上分析アプリです')

# 3. データの読み込み（キャッシュ機能を使って高速化）
@st.cache_data
def load_data():
    # Excelファイルを読み込む
    df = pd.read_excel("sales_report.xlsx", sheet_name="raw_data")
    df["total_sales"] = df["price"] * df["quantity"]
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# 4. サイドバーを作る（フィルタリング機能）
st.sidebar.header("Filter Options")

# 日付フィルター
min_date = df["date"].min()
max_date = df["date"].max()

# 日付選択（デフォルトは全期間）
date_range = st.sidebar.date_input(
    "日付範囲を選択",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# ブランド選択フィルター
selected_brands = st.sidebar.multiselect(
    "表示するブランドを選択: ",
    options=df["brand"].unique(),
    default=df["brand"].unique() # 最初は全部選択
)

# dateの中身がちゃんと２つあるか確認する
if len(date_range) == 2:
    start_date, end_date = date_range

    # 選択されたブランドだけでデータを絞り込む
    filtered_df = df[
        (df['brand'].isin(selected_brands)) &
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
        ]
elif len(date_range) == 1:
    st.sidebar.warning("Select the end date.")
    st.stop()

else:
    filtered_df = df

# 5. KPIを表示
total_sales = filtered_df['total_sales'].sum()
total_qty = filtered_df['quantity'].sum()

# 3列のカラムを作って数字を並べる
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"¥{total_sales:,.0f}")
col2.image("https://img.icons8.com/color/48/money-bag.png", width=50)
col2.metric("販売個数", f"{total_qty}units")
col3.metric("データ件数", f"{len(filtered_df)}件")

st.divider()

# 6. グラフの表示エリア
# 画面を２分割
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Brand別シェア")
    fig1 = px.pie(filtered_df, values="total_sales", names="brand", hole=0.4)
    st.plotly_chart(fig1, width='stretch')

with col_chart2:
    st.subheader("商品カテゴリ別売上")
    fig4 = px.treemap(
        filtered_df,
        path=['brand', 'category', 'product'],
        values='total_sales',
        color='total_sales',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig4, width='stretch')

# 7. Raw Dataの表示
if st.checkbox("Show raw data"):
    st.dataframe(filtered_df)