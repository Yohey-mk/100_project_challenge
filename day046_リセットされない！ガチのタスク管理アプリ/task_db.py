# task_db.py
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Persistent Task Manager", layout="centered")
st.title("💾 リセットされない！ガチのタスク管理アプリ")
st.markdown("SQLiteデータベースを使って、ブラウザを閉じても消えないタスク管理を作ります！")

# 1. データベースの準備
conn = sqlite3.connect('tasks.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          task TEXT NOT NULL
          )
''')
conn.commit() # 変更を保存

# 2. Streamlitのフォーム機能を使い、タスクの追加
st.subheader("📝 新しいタスクの追加")
# with st.formを使うとエンターや追加ボタンを押すまで画面がリロードされない
with st.form(key='add_form', clear_on_submit=True):
    new_task = st.text_input("タスクを入力してください")
    submit_button = st.form_submit_button(label='追加')

    if submit_button and new_task:
        c.execute('INSERT INTO tasks (task) VALUES (?)', (new_task,))
        conn.commit()
        st.success(f"{new_task}を追加しました！")
        st.rerun()

# 3. タスクの表示と削除
st.markdown("---")
st.subheader("📋 現在のタスク一覧")

# データベースからすべてのタスクを選択（取得）する
c.execute('SELECT * FROM tasks')

tasks = c.fetchall()

if not tasks:
    st.info("現在登録されているタスクはありません")
else:
    for task_id, task_name in tasks:
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.write(f"・{task_name}")

        with col_btn:
            if st.button("完了", key=f"del_{task_id}", type="primary"):
                c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
                conn.commit()
                st.rerun()

# 最後にデータベースとの接続を閉じる
conn.close()