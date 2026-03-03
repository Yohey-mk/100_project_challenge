# nlp_dashboard.py

import os
# OSの言語設定を汎用的な「C.UTF-8」に強制的に固定し、Streamlit Cloudで動くか確認
os.environ["LC_ALL"] = "en_US.UTF-8"
os.environ["LANG"] = "en_US.UTF-8"

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
stopwords_file = st.file_uploader("追加でSTOPWORDSがある場合はアップロードしてください", type=['csv', 'xlsx'])

if stopwords_file:
    if stopwords_file.name.endswith('.csv'):
        df_stop = pd.read_csv(stopwords_file)
    else:
        df_stop = pd.read_excel(stopwords_file)

    # 1列目のデータを文字列にしてリスト化（欠損値は除外）
    new_stopwords = df_stop.iloc[:, 0].dropna().astype(str).tolist()

    # set(集合)に複数の単語を一気に追加するためにupdateを使う
    STOP_WORDS.update(new_stopwords)
    st.success(f"{len(new_stopwords)}個のストップワードを追加しました！")

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("データの読み込みに成功しました！")

    columns_list = df.columns.tolist()
    text_col = st.selectbox("分析したいテキストのカラム（列）を選択してください", options=columns_list)

    df_clean = df.dropna(subset=[text_col]).copy()

    st.divider()

    # ===========
    # 分析結果を記憶する箱を作る
    # ===========
    if "analyzed_df" not in st.session_state:
        st.session_state['analyzed_df'] = None

    # ===========
    # 準備：先に全データの感情分析を終わらせる
    # ===========
    # 処理中であることをユーザに伝えるSpinnerを使う
    if st.button(label="感情分析を開始", type="primary"):
        with st.spinner("感情分析を実行中... 少々お待ちください..."):
            def get_sentiment(text):
                res = sonar.ping(text=str(text))
                top_class = res['top_class']

                confidence = 0
                for item in res['classes']:
                    if item['class_name'] == top_class:
                        confidence = item['confidence']
                        break
                if confidence < 0.6:
                    return "Neutral(ニュートラル)"
                elif top_class == "positive":
                    return "Positive(ポジティブ)"
                else:
                    return "Negative(ネガティブ)"
            
            # 先にSentimentカラムを作っておく
            df_clean['Sentiment'] = df_clean[text_col].apply(get_sentiment)

            # 分析が終わったデータをsession_stateに保存（記憶）する
            st.session_state['analyzed_df'] = df_clean

    # ===========
    # 記憶の中にデータがあれば（=分析が完了していれば）、UIを表示する
    # ===========
    if st.session_state['analyzed_df'] is not None:
        # 記憶していたデータを取り出して使う
        df_result = st.session_state['analyzed_df']

        # ===========
        # フィルター機能（UI）
        # ===========
        st.subheader("🔍 分析対象の絞り込み")
        # ラジオボタンでフィルターの選択肢を作る
        filter_option = st.radio(
            "どの感情のコメントでWord Cloudを作りますか？",
            options=['すべて', 'Positive(ポジティブ)', 'Negative(ネガティブ)', 'Neutral(ニュートラル)'],
            horizontal=True
        )

        # 選んだフィルターに応じてデータを絞り込む
        if filter_option == "すべて":
            df_filtered = df_result.copy()
        else:
            # df_cleanの中から、Sentimentが選んだ感情（filter_option）と一致する行だけを残す
            df_filtered = df_result[df_result['Sentiment'] == filter_option].copy()

        st.write(f"該当するコメント数: {len(df_filtered)}件")

        col1, col2 = st.columns(2)

        # ===========
        # 左側：Word Cloudの生成（絞り込んだデータを使う）
        # ===========
        with col1:
            st.subheader(f"☁️ Word Cloud ({filter_option})")

            # 絞り込んだあとのデータ（df_filtered）を使って結合する
            if len(df_filtered) > 0:
                #all_text = " ".join(df_filtered[text_col].astype(str).tolist())
                words = []

                # all_textをやめて、1行ずつループで回して解析する
                for comment in df_filtered[text_col].astype(str).tolist():
                    # 空のコメントなどはスキップ
                    if not comment.strip():
                        continue

                    # 1コメントごとに形態素解析
                    for m in tokenizer.tokenize(comment):
                        pos = m.part_of_speech()[0]
                        word_base = m.dictionary_form()
                        # 品詞のチェックに加えて単語がストップワードに入っていないかチェック
                        if pos in {"名詞", "形容詞", "動詞", "副詞"} and word_base not in STOP_WORDS:
                            words.append(word_base)
                # all_textを使っていたときの処理（for loopの中身は同じ）、学びの記録として残す
                # for m in tokenizer.tokenize(all_text):
                #    pos = m.part_of_speech()[0]
                #    word_base = m.dictionary_form()
                #
                #    # 品詞のチェックに加えて単語がストップワードに入っていないかチェック
                #    if pos in {"名詞", "形容詞", "動詞", "副詞"} and word_base not in STOP_WORDS:
                #        words.append(word_base)

                if len(words) > 0:
                    wakati_text = " ".join(words)
                    font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"

                    wordcloud = WordCloud(
                        width=1920,
                        height=1080,
                        background_color='white',
                        font_path=font_path
                    ).generate(wakati_text)

                    fig_wc, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig_wc)
                else:
                    st.warning("表示できる有効な単語が見つかりませんでした。")
            else:
                st.warning("この感情に分類されたコメントはありません。")

        # ===========
        # 右側：ネガポジ分析の円グラフ（常に全体のデータを使う）
        # ===========
        with col2:
            st.subheader("📊 全体の感情割合")

            # 円グラフでは常に全体を見たいので、df_cleanのまま集計する
            sentiment_counts = df_result['Sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['Sentiment', 'Count']

            fig_pie = px.pie(
                sentiment_counts,
                values='Count',
                names='Sentiment',
                hole=0.4,
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
        st.write(f"{filter_option}のコメント一覧")
        st.dataframe(df_filtered[[text_col, 'Sentiment']])
