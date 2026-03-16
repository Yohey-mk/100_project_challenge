# frontend_todo.py

import streamlit as st
import requests

st.set_page_config(page_title="ToDo App", layout="centered")
st.title("🚀 フルスタック・タスク管理アプリ")

# FastAPIのベースURL（uvicornで立ち上げたアドレス）
API_URL = "http://127.0.0.1:8000"

# 1. タスクの追加（Streamlit -> FastAPIへPOST）
st.subheader("📝 新しいタスクの追加")
with st.form(key='add_form', clear_on_submit=True):
    new_title = st.text_input("タスク名")
    new_description = st.text_input("詳細(任意)")
    submit_button = st.form_submit_button(label='追加')

    if submit_button and new_title:
        # 送信するデータを辞書型でまとめる
        payload = {"title": new_title, "description": new_description}
        # requestsライブラリを使って、APIにデータを送信する(json引数にpayloadを渡す)
        response = requests.post(f"{API_URL}/tasks/", json=payload)

        # HTTPステータスコードが成功（200番台）であることを確認するプロパティ
        if response.status_code == 200:
            st.success("タスクを追加しました！")
        else:
            st.error("追加に失敗しました...")
        st.rerun()

# 2. タスク一覧の取得 (Streamlit <- FastAPIからGET)
st.markdown("---")
st.subheader("📋 現在のタスク一覧")

# requestsライブラリを使ってAPIからデータを取得（GET）
response = requests.get(f"{API_URL}/tasks/")

if response.status_code == 200:
    tasks = response.json()
    if not tasks:
        st.info("タスクはありません。")
    else:
        for task in tasks:
            with st.expander(f"📌 {task['title']}"):
                st.write(task.get('description') or "詳細なし")

                if st.button("完了にする", key=f"btn_{task['id']}"):
                    st.toast(f"ID:{task['id']}を完了しました！")
else:
    st.error("APIサーバに接続できません。FastAPIが起動している確認してください。")