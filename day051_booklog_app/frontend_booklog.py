# frontend_booklog.py
import streamlit as st
import requests

st.set_page_config("My Reading Log", layout="centered", page_icon="📚")
st.title("📚自分だけの読書読書ログ")

API_URL = "http://127.0.0.1:8000"

# 1. 新しい本の登録フォーム
st.subheader("✏️ 新しい本を記録する")

with st.form(key='book_form', clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        new_title = st.text_input("本のタイトル")
    with col2:
        new_author = st.text_input("著者名")

    new_rating = st.slider("評価（1~5）", min_value=1, max_value=5, value=3)
    new_review = st.text_area("感想")
    new_emotion = st.selectbox("読後の感情", ["☺️ (ほっこり)", "😂 (爆笑)", "😡 (憤り)", "☹️ (ビミョー)", "🤯 (衝撃)", "🥺 (感動)"])

    submit_button = st.form_submit_button(label="記録を保存する")

    if submit_button and new_title:
        emotion_emoji = new_emotion[0] # 絵文字と文字が合体しているので、最初の一文字（絵文字部分）だけを切り取る

        payload = {
            "title": new_title,
            "author": new_author,
            "rating": new_rating,
            "review": new_review,
            "emotion": emotion_emoji
        }

        response = requests.post(f"{API_URL}/books/", json=payload)

        if response.status_code == 200:
            st.success("読書記録を保存しました！")
        else:
            st.error("保存に失敗しました...")
        st.rerun()

# 2. 読書ログ一覧の表示
st.markdown("---")
st.subheader("📖 これまでの読書記録")

response = requests.get(f"{API_URL}/books/")

if response.status_code == 200:
    books = response.json()

    if not books:
        st.info("まだ記録がありません。最初の本を登録してみましょう！")
    else:
        for book in reversed(books): # 新しい記録が上に来るように、リストを逆順にする
            stars = "⭐" * book['rating'] # 評価の数だけ⭐️を表示する

            with st.container(border=True):
                st.markdown(f"### {book['emotion']} {book['title']}")
                st.markdown(f"**著者:** {book['author']} | **評価:** {stars}")
                st.markdown(f"> {book['review']}")

else:
    st.error("APIサーバに接続できません。バックエンドが起動しているか確認してください。")