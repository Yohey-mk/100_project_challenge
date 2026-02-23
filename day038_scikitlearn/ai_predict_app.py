# ai_predict_app.py

import streamlit as st
import pandas as pd
import joblib
# import pickle

st.set_page_config(page_title="AI内定シミュレータ", layout="centered")
st.title("AI内定予測シミュレータ")
st.markdown("あなたの現在のスコアを入力すると、過去10万人のデータからAIが内定/未内定かを予測します")

# 1. 保存したAIモデルとカラム情報を読み込む
@st.cache_resource
def load_ai_model():
    loaded_model = joblib.load('day038_scikitlearn/rf_model.pkl')
    loaded_columns = joblib.load('model_columns.pkl')
    return loaded_model, loaded_columns

model, model_columns = load_ai_model()

# 2. ユーザに入力してもらうUIを作成する
st.subheader("あなたのスコアを入力してください")

col1, col2 = st.columns(2)

with col1:
    mock_score = st.number_input("模擬面接スコア（0-100）", min_value=0.0, max_value=100.0, value=70.0)
    coding_score = st.number_input("コーディングスキル（0-100）", min_value=0.0, max_value=100.0, value=70.0)
    cgpa = st.number_input("学業成績（0-10）", min_value=0.0, max_value=10.0, value=7.0)

with col2:
    aptitude_score = st.number_input("適性検査スコア（0-100）", min_value=0.0, max_value=100.0, value=70.0)
    logical_score = st.number_input("論理的思考力（0-100）", min_value=0.0, max_value=100.0, value=70.0)
    comm_score = st.number_input("コミュニケーション力（0-100）", min_value=0.0, max_value=100.0, value=70.0)

# 3. 予測ボタンが押された時の処理
if st.button("AIで結果を予測する", type="primary"):
    # 入力されたデータをDataFrameにする
    input_data = pd.DataFrame({
        'mock_interview_score': [mock_score],
        'coding_skill_score': [coding_score],
        'cgpa': [cgpa],
        'aptitude_score': [aptitude_score],
        'logical_reasoning_score': [logical_score],
        'communication_skill_score': [comm_score]
    })

    # ユーザが入力していない他の特徴は0で埋めて、学習時と全く同じ列の形（model_columns）に整える（reindex関数）
    input_data_encoded = pd.get_dummies(input_data)
    input_data_encoded = input_data_encoded.reindex(columns=model_columns, fill_value=0)

    # 読み込んだAIモデルを使って予測を実行
    prediction = model.predict(input_data_encoded)

    # predict_proba()を使って確率を出す
    probabilities = model.predict_proba(input_data_encoded)
    # probabilitiesは[[未内定の確率, 内定の確率]]という二次元のリストで返ってくるので、二番目の確率を取り出す
    placed_prob = probabilities[0][1]
    placed_prob_percent = placed_prob * 100

    # 結果を表示
    st.divider()
    st.metric("あなたの内定獲得確率", f"{placed_prob_percent:.1f}%")

    if prediction[0] == "Placed":
        st.success("おめでとうございます！AIの予測結果は内定です！")
        st.balloons()
    else:
        st.error("残念ながら、現在のスコアでの予測は未内定です。模擬面接のスコアを上げてみましょう！")
        if placed_prob_percent >= 40:
            st.warning("あともう一息！他に点数を上げることができそうな項目を探してみましょう。")