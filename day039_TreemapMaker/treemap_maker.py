# treemap_maker.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="汎用Treemapメーカー", layout="wide")
st.title("汎用Treemapメーカー")
st.markdown("どんなExcelファイルでも、項目を割り当てるだけでツリーマップを作成できます！")

# 1. ファイルのアップロード機能
# st.file_uploaderを使ってファイルをアップロードできるようにする
uploaded_file = st.file_uploader("Excel / CSVファイルをアップロードしてください", type=["xlsx", "csv"])

if uploaded_file is not None:
    # ファイル形式に応じて読み込む
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("ファイルの読み込みに成功しました！")

    # 2. エクセルファイルの1行目（項目=カラム）一覧を表示する
    st.subheader("①読み込んだデータの項目（カラム）一覧")

    # 読み込んだDataFrame（df）からカラム名の一覧を取り出します
    # df.columnsを使う
    columns_list = df.columns.tolist()

    # 画面に横並びで表示する
    st.write("検出された項目：", columns_list)

    # 3. 項目のマッピング
    st.subheader("②ツリーマップの設定")
    st.markdown("面積の基準となる「数値データ（売上など）」と、階層の基準となる「項目データ（ブランド、カテゴリなど）を選んでください」")

    col1, col2 = st.columns(2)

    with col1:
        # 面積の基準（数値）を選ぶ
        value_col = st.selectbox("面積の基準を選択", options=columns_list)

    with col2:
        # 階層を選ぶ. multiselectで「親から順に選ぶ」形式にする
        hierarchy_cols = st.multiselect(
            "階層にしたい項目を親から順に選んでください（例：ブランド→カテゴリ→商品名）：",
            options=columns_list
        )

    # 4. Treemapの作成と表示
    if st.button("Treemapを作成する", type="primary"):
        if len(hierarchy_cols) == 0:
            st.error("階層項目を1つ以上選んでください")
        else:
            # Treemapを作成
            # 階層パス（path）にはhierarchy_colsをそのまま渡す
            # 値（values）には選んだvalue_colを渡す
            fig = px.treemap(
                df,
                path=hierarchy_cols,
                values=value_col,
                title="カスタムツリーマップ"
            )

            # 作ったグラフをStreamlitに表示する
            st.plotly_chart(fig, width='stretch')
    # 生データの表示
    st.divider()
    if st.checkbox("生データを表示"):
        st.dataframe(df)

else:
    st.info("上の枠にファイルをアップロードしてください")
