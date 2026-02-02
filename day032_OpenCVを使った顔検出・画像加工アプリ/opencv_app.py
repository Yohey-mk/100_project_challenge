# opencv_app.py

import cv2
import numpy as np

# 画像を重ね合わせる関数
def overlay_image(bg_img, fg_img, x_pos, y_pos):
    """
    bg_img: 背景画像（カメラ映像）
    fg_img: 前景画像（サングラスなど、透過PNG）
    x_pos, y_pos: 貼り付ける左上の座標
    """
    # 1. 画像のサイズを取得
    h, w = fg_img.shape[:2]

    # 2. 背景画像からはみ出さないように範囲を調整（画面端の処理）
    if x_pos < 0 or y_pos < 0 or x_pos + w > bg_img.shape[1] or y_pos + h > bg_img.shape[0]:
        return bg_img # はみ出す場合は何もしない
    
    # 3. 貼り付ける場所の背景画像を取り出す（ROI）
    roi = bg_img[y_pos : y_pos + h, x_pos : x_pos + w]

    # 4. アルファチャンネル（透明度）と色チャンネルを分離
    # fg_img[:, :, :3] -> 色情報（BGR）
    # fg_img[:, :, 3] -> 透明度情報（Alpha）0 ~ 255
    img = fg_img[:, :, :3]
    mask = fg_img[:, :, 3]

    # 5. マスクを0~1の範囲に正規化（計算しやすくする）
    mask = mask / 255.0

    # 6. 合成処理（アルファブレンド）
    # (1 - mask)はサングラスがない部分（背景を生かす）
    # maskはサングラスがある部分
    # shapeを(h, w, 1)に変換して掛け算できるようにする
    mask = mask[:, :, np.newaxis]

    # 背景 * (1 - alpha) + sunglasses * alpha
    result = (roi * (1.0 - mask) + img * mask).astype(np.uint8)

    # 7. 計算結果を元の背景画像に戻す
    bg_img[y_pos : y_pos + h, x_pos : x_pos + w] = result

    return bg_img

# Main 処理
# サングラスの画像を読み込む（第二引数 -1 はIMREAD_UNCHANGED = アルファチャンネルも含めて読む）
glass_img_orig = cv2.imread("sunglasses.png", -1)

if glass_img_orig is None:
    print("画像が見つかりません。'sunglasses.png'を確認してください。")
    exit()
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
        # サングラスのリサイズと位置調整
        # 顔の幅に合わせてサングラスをリサイズ
        # 少し大きめに調整したい場合は w * 1.1 などにする
        glass_width = w * 1.05
        # 元の縦横比を維持して高さを計算
        glass_height = int(glass_img_orig.shape[0] * (glass_width / glass_img_orig.shape[1]))

        # リサイズ実行
        glass_resized = cv2.resize(glass_img_orig, (int(glass_width), int(glass_height)))
        
        # 目の位置あたりに調整（y座標を少し下げる、xはそのまま）
        glass_y = y + int(h * 0.20)
        glass_x = x

        # 作成した関数を呼び出して合成
        frame = overlay_image(frame, glass_resized, glass_x, glass_y)

#        # A. 顔の領域（ROI: Region Of Interest）を切り出す
#        face_roi = frame[y : y+h, x : x+w]

#        # B. モザイク処理
#        # 1. 情報を間引く（1/10に縮小）
#        small_face = cv2.resize(face_roi, None, fx=0.03, fy=0.03, interpolation=cv2.INTER_NEAREST)
#        # 2. 元の大きさに戻す（拡大）
#        # cv2.INTER_NEAREST(最近傍法)を使うと、ドット絵のようになる
#        mosaic_face = cv2.resize(small_face, (w, h), interpolation=cv2.INTER_NEAREST)

#        # C. 元の画像に貼り戻す
#        frame[y : y+h, x : x+w] = mosaic_face

#        # 赤枠線も学びの記録として残しておくcv2.rectangle(画像, 左上座標, 右下座標, 色（BGR）, 線の太さ)
#        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 7. 結果を画面に表示する
    cv2.imshow('Face Detector', frame)

    # 9. 'q'キーが押されたらループを抜ける
    # waitKey(1)は1ミリ秒キー入力を待つ関数
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 終了処理
cap.release()
cv2.destroyAllWindows