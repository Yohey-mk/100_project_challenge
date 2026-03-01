# nlp_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import sudachipy
from asari.api import Sonar

sudachi_dict = sudachipy.Dictionary()
sonar = Sonar()
tokenizer = sudachi_dict.create(mode=sudachipy.SplitMode.C)

# test用なのでコメントアウト
#text = "吾輩は猫である"
#sudachi_tokenize = tokenizer.tokenize(text)

# Asariでの感情分析テスト
#res = sonar.ping(text="マジありえないわ〜") # {'text': 'textcontents', 'top_class': 'negative',...} -> top_classを感情判定で取り出すようにする

#print(sudachi_tokenize)
#print(res)

# 0. Initial Setup
st.set_page_config(page_title="NLPコメント分析ツール", layout="wide")
st.title("💬 NLPコメント分析＆Word Cloudメーカー")
st.markdown("テキストを読み込み、頻出単語の可視化と感情分析を行います")


# 1. ファイルアップロード
uploaded_file = st.file_uploader("CSV/Excelファイルをアップロードしてください", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("データの読み込みに成功しました！")

    # テキストが入っているカラムを選択させる
    columns_list = df.columns.tolist()
    text_col = st.selectbox("分析したいテキストのカラム（列）を選択してください", options=columns_list)

    # 欠損値を削除し、綺麗なデータにしておく
    df_clean = df.dropna(subset=[text_col]).copy()

    st.divider()

    col1, col2 = st.columns(2)

    # Word Cloudの生成
    with col1:
        st.subheader("☁️ Word Cloud")
        # df_clean[text_col]のすべての行のテキストをスペースで結合（join）し、ワードクラウド生成する
        all_text = " ".join(df_clean[text_col].astype(str).tolist())

        # SudachiPyで形態素解析（分かち書き）を行う
        words = []
        # tokenizerにコードの最初で定義したtokenizer.tokenizeを使う
        for m in tokenizer.tokenize(all_text):
            pos = m.part_of_speech()[0] # 品詞を取得
            # 意味のある単語（名刺、形容詞、動詞、副詞）だけを抽出する
            if pos in {"名詞", "形容詞", "動詞", "副詞"}:
                words.append(m.dictionary_form())
        # 抽出した単語リストをスペースで結合しなおす
        wakati_text = " ".join(words)

        # WordCloudを生成
        font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            font_path=font_path).generate(wakati_text)

        # StreamlitでMatplotlibの図を表示する準備
        fig_wc, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off") # 軸を消す

        st.pyplot(fig_wc)

    # ネガポジ分析
    with col2:
        st.subheader("📊 感情分析（ネガポジ判定）")

        def get_sentiment(text):
            # 1. 渡された「１行分のテキスト」をAsariで解析する
            res = sonar.ping(text=str(text))
            top_class = res['top_class']

            # 2. 辞書の中から「自信度」を取り出す
            confidence = 0
            for item in res['classes']:
                if item['class_name'] == top_class:
                    confidence = item['confidence']
                    break
            
            # 3. 判定ロジック（自信度が60％未満ならニュートラル）
            if confidence < 0.6:
                return "Neutral(ニュートラル)"
            elif top_class == "positive":
                return "Positive(ポジティブ)"
            else:
                return "Negative(ネガティブ)"

        # df_cleanに新しいカラム'Sentiment'を作り、get_sentimentをapplyする
        df_clean['Sentiment'] = df_clean[text_col].apply(get_sentiment)

        # 感情の数を集計する
        sentiment_counts = df_clean['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']

        # Plotly ExpressでPie chartを作る
        fig_pie = px.pie(
            sentiment_counts,
            values='Count',
            names='Sentiment',
            hole=0.4,
            title="コメントの感情割合",
            color='Sentiment',
            color_discrete_map={
                "Positive(ポジティブ)": "lightgreen",
                "Negative(ネガティブ)": "salmon",
                "Neutral(ニュートラル)": "lightgray"
            }
        )

        st.plotly_chart(fig_pie, width='stretch')

    # プレビュー表示
    st.divider()
    st.write("📝 分析結果データ（一部）")
    st.dataframe(df_clean[[text_col, 'Sentiment']].head(50))