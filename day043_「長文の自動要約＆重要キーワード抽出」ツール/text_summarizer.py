# text_summarizer.py

import streamlit as st
import pandas as pd
import numpy as np
from sudachipy import tokenizer
from sudachipy import dictionary
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from asari.api import Sonar # 要約したテキストの感情分析を行う（Extra challenge）

st.set_page_config(page_title="Text Summarizer", layout='wide')
st.title("📝 長文要約＆キーワード抽出ツール")

# --- 1. SudachiPyの準備 ---
@st.cache_resource
def setup_tokenizer():
    sudachi_dict = dictionary.Dictionary()
    return sudachi_dict.create(mode=tokenizer.Tokenizer.SplitMode.C)

tk = setup_tokenizer()

def tokenize_text(text):
    """文章を単語に分割し、名刺動詞形容詞だけを抽出し、スペース区切りの文字列にする関数"""
    tokens = []
    for m in tk.tokenize(text):
        pos = m.part_of_speech()[0] # pos = Part Of Speech
        if pos in ["名詞", "動詞", "形容詞"]:
            tokens.append(m.dictionary_form()) # 単語の表層形を取得する
    return " ".join(tokens)

sonar = Sonar()
def get_sentiment(text):
    res = sonar.ping(text=str(text))
    top_class = res['top_class']
    confidence = 0
    for item in res['classes']:
        if item['class_name'] == top_class:
            confidence = item['confidence']
            break
    if confidence < 0.4:
        return "Neutral(ニュートラル)"
    elif top_class == "positive":
        return "Positive(ポジティブ)"
    else:
        return "Negative(ネガティブ)"

# --- 2. UIの構築 ---
st.markdown("ニュース記事などの長文を貼り付けてください")
source_text = st.text_area("テキスト入力", height=200)

if st.button("文章を解析する"):
    if len(source_text) == 0:
        st.warning("テキストを入力してください。")
    else:
        with st.spinner("解析中..."):
            # --- 3. 文章の分割 ---
            sentences = source_text.split("。")

            # 空の文字列を除外する(「。」で終わっていると最後が空になるため)
            sentences = [s + "。" for s in sentences if len(s.strip()) > 0]

            # 各文をトークン化（単語に分割）
            tokenized_sentences = [tokenize_text(s) for s in sentences]

            # --- 4. TF-IDFによるキーワード抽出 ---
            vectorizer = TfidfVectorizer() # TfidVectorizerのインスタンス作成
            # トークン化された文のリストを元にTF-IDFを計算（学習と変換を同時に行う）
            tfidf_matrix = vectorizer.fit_transform(tokenized_sentences)

            # --- キーワードTop５を抽出 ---
            feature_names = vectorizer.get_feature_names_out()
            # 全文のスコアを合計
            total_scores = tfidf_matrix.sum(axis=0).A1
            # スコアが高い順のインデックスを取得
            top_keyword_indices = np.argsort(total_scores)[::-1][:5]
            top_keywords = [feature_names[i] for i in top_keyword_indices]

            st.subheader("🔑 重要キーワード Top 5")
            # 抽出したキーワードをカンマ区切りで表示
            st.info(" / ".join(top_keywords))

            # --- 5. 重要文の抽出（要約） ---
            # 各文の「重要度スコア」（その文に含まれるTF-IDF値の合計）を計算
            sentence_score = tfidf_matrix.sum(axis=1).A1

            # numpyを使ってsentence_scoresが高い順にソートし上位３つのインデックスを取得
            top_sentence_indices = np.argsort(sentence_score)[::-1][:3]

            # 選ばれた3文を元の文章の登場順に並べ直す
            top_sentence_indices.sort()

            st.subheader("📄 AIによる3行要約")
            for i, idx in enumerate(top_sentence_indices):
                st.write(f"**{i+1}.** {sentences[idx]}")
            
            st.subheader("感情解析結果")
            # sentencesから文章を取り出し、１つのテキストに合体して渡す
            summary_sentences = [sentences[idx] for idx in top_sentence_indices]
            summary_text = "".join(summary_sentences)
            sentiment_analysis = get_sentiment(summary_text)
            st.write(sentiment_analysis)
        st.success("解析が完了しました")
