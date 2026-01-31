# Day31 Heart Disease Predictor on Streamlit
import streamlit as st
import pandas as pd
import joblib

# 1. 保存したモデルを読み込む
model = joblib.load("my_model.joblib")

# 2. User Interface
st.title("Heart Disease Predictor")
age = st.number_input(label="Enter your age", max_value=120, min_value=0)
sex = st.selectbox(label="Select your gender", options=["Male", "Female"])
chestpaintype = st.selectbox(label="Select your chestpain type", options=["typical angina", "asymptomatic", "atypical angina","non-anginal"])
restingbp = st.number_input(label="Resting Blood Pressure", max_value=300, min_value=0)
cholesterol = st.number_input(label="Cholesterol Level", max_value=500, min_value=0)
fbs = st.selectbox(label="Fasting Blood Sugar Level\n(If FBS > 120, select True)", options=["True", "False"])
restecg = st.selectbox(label="Resting Electrocardiographic Results", options=["lv hypertrophy", "normal"])
maxhr = st.number_input(label="Max Heart Rate", max_value=300, min_value=0)
exang = st.selectbox(label="Exercise-induced angina(If you experience chest pain or discomfort during physical exertion, select True)", options=["True", "False"])
oldpeak = st.number_input(label="Oldpeak(the amount of ST segment depression)", max_value=float(10.0), min_value=float(0))
slope = st.selectbox(label="ST/heart rate", options=["downsloping", "flat", "upsloping"])
ca = st.number_input(label="CA (between 0 - 10)", max_value=10, min_value=0)
thal = st.selectbox(label="Thalach(maximum heart rate achieved during exercise)", options=["fixed detect", "normal", "reversable detect"])

# 3. Run prediction
if st.button(label="Run prediction"):
    # A. カテゴリ変数を数字に変換する準備
    sex_mapping = {"Male": 1, "Female": 0}
    chestpaintype_mapping = {"asymptomatic": 0, "atypical angina": 1, "non-anginal": 2, "typical angina": 3}
    fbs_mapping = {"False": 0, "True": 1}
    restecg_mapping = {"lv hypertrophy": 0, "normal": 1}
    exang_mapping = {"False": 0, "True": 1}
    slope_mapping = {"downsloping": 0, "flat": 1, "upsloping": 2}
    thal_mapping = {"fixed detect": 0, "normal": 1, "reversable detect": 2}

    # B. モデルに渡すデータを１つの辞書にまとめる
    input_data = {
        'Age': age,
        'Sex': sex_mapping[sex],
        'ChestPainType': chestpaintype_mapping[chestpaintype],
        'RestingBP': restingbp,
        'Cholesterol': cholesterol,
        'fbs': fbs_mapping[fbs],
        'restecg': restecg_mapping[restecg],
        'MaxHR': maxhr,
        'exang': exang_mapping[exang],
        'Oldpeak': oldpeak,
        'slope': slope_mapping[slope],
        'ca': ca,
        'thal': thal_mapping[thal],
    }
    # C. 辞書をDataFrame（１行だけの表）に変換する（pd.DataFrame([dict])とすることでモデルに渡せる形にする）
    input_df = pd.DataFrame([input_data])

    # Debug
    st.write("モデルに入力されるデータ")
    st.dataframe(input_df)

    # D. 予測実行
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df) # [0の確率, 1の確率] *0=No hd risk, 1=hd risk

    # 結果表示
    st.subheader("診断結果")
    # 病気あり(1)の確率を取得
    risk_score = probability[0][1]
    if prediction[0] == 1:
        st.error(f"Heart Disease Detected (Risk {risk_score:.2%})")
        st.write("心臓病リスクあり。専門医の受信をお勧めします。")
    else:
        st.success(f"Healthy (Risk: {risk_score:.2%})")
        st.write("心臓病のリスクは低いと予測されました。")
