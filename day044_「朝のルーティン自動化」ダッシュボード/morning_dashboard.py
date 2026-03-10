# morning_dashboard.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime

st.set_page_config(page_title="Morning Dashboard", layout="wide")
st.title("🌅 My Morning Dashboard")

# --- 1. 日付の表示 ---
now = datetime.datetime.now()
st.subheader(f"今日は{now.strftime('%Y年%m月%d日')}です！")

st.markdown("---")

col1, col2, col3 = st.columns(3)

# --- Left column：天気情報 ---
with col1:
    st.header("🌤 今日の天気 (福岡)")

    # Open-Meteo APIを使う
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=33.5902&longitude=130.4017&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=Asia%2FTokyo"

    try:
        res_weather = requests.get(weather_url)
        weather_data = res_weather.json()
        max_temp = weather_data['daily']['temperature_2m_max'][0]
        min_temp = weather_data['daily']['temperature_2m_min'][0]
        st.metric(label="最高 / 最低気温", value=f"{max_temp}℃ / {min_temp}℃")
    except Exception as e:
        st.error(f"天気情報の取得に失敗しました：{e}")

# --- Right Column：ニュース情報 ---
with col2:
    st.header("📰 最新ITニュース")

    news_url = "https://news.yahoo.co.jp/rss/topics/it.xml"

    try:
        res_news = requests.get(news_url)
        soup = BeautifulSoup(res_news.content, "lxml-xml")
        items = soup.find_all("item")

        for item in items[:5]:
            title = item.title.text
            link = item.link.text

            st.markdown(f"- [{title}]({link})")
    
    except Exception as e:
        st.error(f"ニュースの取得に失敗しました：{e}")

# --- EXTRA Challenge ---
# ToDo Listを作ってみよう
with col3:
    st.header("⏰️ToDo List")

    # 1. もしsession_stateの中に'todos'というリストがなければ新しく空のリストを作る
    if 'todos' not in st.session_state:
        st.session_state['todos'] = []

    def pop_todos(i):
        st.session_state['todos'].pop(i)

    # 2. ToDoを追加する入力欄とボタン
    new_todo = st.text_input("新しいタスクを入力してください")
    if st.button("追加"):
        if new_todo:
            st.session_state['todos'].append(new_todo)
            # 画面を強制的にリロードして最新状態にする
            st.rerun()
    
    # 3. 現在のToDoを箇条書きで表示
    for i, task in enumerate(st.session_state['todos']):
        # チェックボックスを表示
        st.checkbox(task, key=f"todo_{i}")
        st.button("Delete",
                  type="tertiary",
                  on_click=pop_todos,
                  args=[i],
                  key=f"delete_{i}")