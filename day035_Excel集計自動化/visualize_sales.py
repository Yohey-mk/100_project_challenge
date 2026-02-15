# visualize_sales.py

import pandas as pd
import plotly.express as px
import numpy as np

# 1. Dataの読み込み
print("Excelファイルを読み込み中...")
df = pd.read_excel("sales_report.xlsx", sheet_name="raw_data")

df["total_sales"] = df["price"] * df["quantity"]

# グラフ1: ブランドxカテゴリの売上構成（サンバースト図）
# 中心から「ブランド」→「カテゴリ」→「商品」と階層的に内訳が見れる
fig1 = px.sunburst(
    df,
    path=['brand', 'category', 'product'], # 階層を指定
    values='total_sales', # サイズの基準
    title='🏆 ブランド・カテゴリ別 売上構成比 (クリックでズームできます)',
    color='brand',
    height=700
)
fig1.show()

# グラフ2: 価格帯と販売数の関係（散布図）
# 「高いけど売れている商品」、「安くて大量に売れている商品」を見つける
fig2 = px.scatter(
    df,
    x='price',
    y='quantity',
    size='total_sales',
    color='brand',
    hover_data=['product', 'color'],
    title='price vs units'
)
fig2.show()

# グラフ3: 人気カラーランキング
# 何色が一番売れているか集計する
color_summary = df.groupby('color')['total_sales'].sum().reset_index()
color_summary = color_summary.sort_values('total_sales', ascending=False)

fig3 = px.bar(
    color_summary,
    x='color',
    y='total_sales',
    color='total_sales',
    title='カラー別売り上げランキング',
    text_auto=True
)
fig3.show()

fig4 = px.treemap(
    df,
    path=['brand', 'product'],
    values='total_sales',
    color='total_sales',
    color_continuous_scale='RdBu',
    color_continuous_midpoint=np.average(df['total_sales'], weights=df['total_sales'])
)
fig4.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig4.show()