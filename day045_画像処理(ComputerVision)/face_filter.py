# face_filter.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Face Filter App", layout="centered")
st.title("🕶️ AI顔認識＆プライバシーフィルター")
st.markdown("画像をアップロードすると、AIが自動で顔を検知してモザイク（ぼかし）をかけます！")

# --- 1. 画像のアップロード ---
upload_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if upload_file is not None:
    # --- 2. 画像の読み込みと変換 ---
    # PIL (Python Image Library)で画像を開く
    image = Image.open(upload_file)
    # 画像データをOpenCVで扱えるようにnumpy配列に変換する
    img_array = np.array(image)
    # AIに顔を探させるために画像を白黒（グレースケール）に変換する
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    # --- 3. AIモデル（Haar Cascade）の準備 ---
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # --- 4. 顔の検出 ---
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    st.info(f"💡 検出された顔の数: {len(faces)} 人")

    # --- 5. 検出された顔にフィルタをかける ---
    # faces には[x, y, w, h]のリストが入っている
    for (x, y, w, h) in faces:
        # img_arrayから顔の部分だけをスライスする
        face_roi = img_array[y: y + h, x: x + w]
        # 切り出したRegion of Interestにガウシアンぼかしをかける
        blurred_face = cv2.GaussianBlur(face_roi, (51, 51), 0)

        # ぼかした顔を元のimg_arrayの同じ位置に代入して上書き
        img_array[y: y+h, x: x+w] = blurred_face

    # --- 6. 結果の表示 ---
    st.image(img_array, caption="フィルタ適用後", width='stretch')
    st.success("処理が完了しました！")