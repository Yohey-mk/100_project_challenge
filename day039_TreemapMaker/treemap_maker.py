# treemap_maker.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="汎用グラフメーカー", layout="wide")
st.title("汎用グラフメーカー")
st.markdown("どんなExcelファイルでも、項目を割り当てるだけでグラフを作成できます！")

graph_options = ['Treemap', 'Bar Chart', 'Pie Chart', 'Donut Chart']

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
    st.subheader("②グラフの設定")
    st.markdown("面積の基準となる「数値データ（売上など）」と、階層の基準となる「項目データ（ブランド、カテゴリなど）を選んでください」")

    col0, col1, col2 = st.columns(3)

    with col0:
        select_graph = st.selectbox("生成したいグラフを選んでください", options=graph_options)

    with col1:
        # 面積の基準（数値）を選ぶ
        if select_graph == "Treemap":
            value_col = st.selectbox("面積の基準を選択", options=columns_list)
        elif select_graph == "Bar Chart":
            y_col = st.selectbox("Y軸（Volume）を選択", options=columns_list)
        elif select_graph == "Pie Chart":
            value_col = st.selectbox("ボリュームを選択（売上など）", options=columns_list)
        elif select_graph == "Donut Chart":
            value_col = st.selectbox("ボリュームを選択（売上など）", options=columns_list)

    with col2:
        # 階層を選ぶ. multiselectで「親から順に選ぶ」形式にする
        if select_graph == "Treemap":
            hierarchy_cols = st.multiselect(
                "階層にしたい項目を親から順に選んでください（例：ブランド→カテゴリ→商品名）：",
                options=columns_list
            )
        elif select_graph == "Bar Chart":
            x_col = st.selectbox("X軸（分類）を選択", options=columns_list)
        elif select_graph == "Pie Chart":
            element_col = st.selectbox("構成要素（ブランドやカテゴリ）を選択", options=columns_list)
        elif select_graph == "Donut Chart":
            element_col = st.selectbox("構成要素（ブランドやカテゴリ）を選択", options=columns_list)


    # 4. Treemapの作成と表示
    if st.button(f"{select_graph}を作成する", type="primary"):
        if select_graph == "Treemap":
            if len(hierarchy_cols) > 0:
                # 階層に選ばれたカラムに空白（NaN）があったら上の値で埋める（ffill）
                # 一番上が空白だった場合、"不明"で埋める（fillna）
                df_clean = df.copy()
                df_clean[hierarchy_cols] = df_clean[hierarchy_cols].ffill().fillna("不明")

                # 念の為、値（売上など）が空っぽの行も0にしておく
                df_clean[value_col] = df_clean[value_col].fillna(0)

                # Treemapを作成
                # 階層パス（path）にはhierarchy_colsをそのまま渡す
                # 値（values）には選んだvalue_colを渡す
                fig = px.treemap(
                    df_clean,
                    path=hierarchy_cols,
                    values=value_col,
                    title="カスタムツリーマップ"
                )
                st.plotly_chart(fig, width='stretch')
            else:
                # Treemapの階層未選択の場合にエラーメッセージを表示する
                st.error("階層項目を１つ以上選んでください")

        elif select_graph == "Bar Chart":
            df_clean = df.copy()
            df_clean[x_col] = df_clean[x_col].ffill().fillna("不明")
            df_clean[y_col] = df_clean[y_col].fillna(0)

            # x_colごとにy_colを合計してスッキリさせる
            df_grouped = df_clean.groupby(x_col, as_index=False)[y_col].sum()

            fig = px.bar(
                df_grouped,
                x=x_col,
                y=y_col,
                text_auto=True
            )
            st.plotly_chart(fig, width='stretch')

        elif select_graph == "Pie Chart" or select_graph == "Donut Chart":
            df_clean = df.copy()
            df_clean[element_col] = df_clean[element_col].ffill().fillna("不明")
            df_clean[value_col] = df_clean[value_col].fillna(0)

            df_grouped = df_clean.groupby(element_col, as_index=False)[value_col].sum()

            if select_graph == "Pie Chart":
                fig = px.pie(
                    df_grouped,
                    values=value_col,
                    names=element_col
                )
                st.plotly_chart(fig, width='stretch')
            elif select_graph == "Donut Chart":
                fig = px.pie(
                    df_grouped,
                    values=value_col,
                    names=element_col,
                    hole=0.4
                )
                st.plotly_chart(fig, width='stretch')

    # 生データの表示
    st.divider()
    if st.checkbox("生データを表示"):
        st.dataframe(df)

else:
    st.info("上の枠にファイルをアップロードしてください")
