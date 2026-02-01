# opencv_app.py

import cv2

# 1. 学習済みの「顔検出器」を読み込む
# opencv-pythonライブラリに含まれているパスを自動で取得
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

# 2. Webカメラを起動する
# 引数の0は内蔵カメラを指す。外付けなら1や2になることもある。
cap = cv2.VideoCapture(1) # MacOS(MacBookAir)だったためか、VideoCapture()には1を指定すると動いた。

if not cap.isOpened():
    print("No camera founds.")
    exit()

print("Running...")

while True:
    # 3. カメラから画像を1フレーム読み込む
    # ret: 読み込み成功したか(True/False), frame: 画像データ(NumPy配列)
    ret, frame = cap.read()

    if not ret:
        break

    # 4. 画像をグレー（白黒）に変換する
    # 顔認識は色の情報より明暗が重要。処理を軽くするため白黒にする。
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 5. 顔を検出
    # scaleFactor: 画像を縮小しながら探す倍率（1.1 = 10%ずつ縮小）
    # minNeighbors: 信頼度の閾値。（数字が大きいほど誤検出減。ただし顔を見逃すこともある。）
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 6. 検出された顔の周りに四角を描く。
    # (x, y, w, h)は(左上のX座標, 左上のY座標, 幅, 高さ)
    for (x, y, w, h) in faces:
        # cv2.rectangle(画像, 左上座標, 右下座標, 色（BGR）, 線の太さ)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 7. 結果を画面に表示する
    cv2.imshow('Face Detector', frame)

    # 9. 'q'キーが押されたらループを抜ける
    # waitKey(1)は1ミリ秒キー入力を待つ関数
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 終了処理
cap.release()
cv2.destroyAllWindows