# nlp_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import sudachipy
from asari.api import Sonar

# 初期設定
sudachi_dict = sudachipy.Dictionary()
sonar = Sonar()
tokenizer = sudachi_dict.create(mode=sudachipy.SplitMode.C)

# Stopword(WordCloudから除外したい無意味な単語)のリスト
STOP_WORDS = {"する", "ある", "いる", "なる", "こと", "もの", "これ", "それ", "あの", "この", "よう", "ない", "れる", "られる", "せる", "させる", "てる", "しまう", "くる", "いく", "みる", "おく", "いい", "よい", "思う", "言う", "できる", "ため", "ん", "の", "さん", "そう"}

# アプリのUI
st.set_page_config(page_title="NLPコメント分析ツール", layout='wide')
st.title("💬 NLPコメント分析＆Word Cloudメーカー")
st.markdown("テキストを読み込み、頻出単語の可視化と感情分析を行います")

uploaded_file = st.file_uploader("CSV/EXCELファイルをアップロードしてください", type=['csv', 'xlsx'])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv()
    else:
        df = pd.read_excel()

    st.success("データの読み込みに成功しました！")

    columns_list = df.columns.tolist()
    text_col = st.selectbox("分析したいテキストのカラム（列）を選択してください", options=columns_list)

    df_clean = df.dropna(subset=[text_col]).copy()

    st.divider()

    # ===========
    # 準備：先に全データの感情分析を終わらせる
    # ===========
    # 処理中であることをユーザに伝えるSpinnerを使う
    with st.spinner("感情分析を実行中... 少々お待ちください..."):
        def get_sentiment(text):
            res = sonar.ping(text=str(text))
            top_class = res('top_class')

            confidence = 0
            for item in res['classes']:
                if item['class_name'] == top_class:
                    confidence = item['confidence']
                    break
            if confidence < 0.6:
                return "Neautral(ニュートラル)"
            elif top_class == "positive":
                return "Positive(ポジティブ)"
            else:
                return "Negative(ネガティブ)"
            
        # 先にSentimentカラムを作っておく
        df_clean['Sentiment'] = df_clean[text_col].apply(get_sentiment)

    # ===========
    # フィルター機能（UI）
    # ===========
    st.subheader("🔍 分析対象の絞り込み")