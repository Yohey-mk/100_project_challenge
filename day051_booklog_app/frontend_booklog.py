# frontend_booklog.py
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config("My Reading Log", layout="wide", page_icon="📚")
st.title("📚自分だけの読書ログ")

# Initial Settings
emotion_list = ["☺️ (ほっこり)", "🤔(学び)","😂 (爆笑)", "😡 (憤り)", "☹️ (ビミョー)", "🤯 (衝撃)", "🥺 (感動)"]
API_URL = "http://127.0.0.1:8000"
response = requests.get(f"{API_URL}/books/")

if response.status_code == 200:
    books = response.json()
    books_list = pd.DataFrame(books)

if books:
    st.subheader("📊あなたの読書統計記録")
    #books_list = pd.DataFrame(books)
    col_log1, col_log2 = st.columns([1,2])
    with col_log1:
        st.metric("総読書数", value=len(books))
        # ratings = [book['rating'] for book in books]と書いてnp.mean()に渡してもよい
        st.metric("平均評価", value=np.around(np.mean(books_list['rating']), 1)) # 小数点以下１位までを表示
    with col_log2: 
        # emotion列だけを取り出して数を数え、グラフ用の新しい表を作成する
        # reset_index(name='count')を使い、['emotion', 'count']というPlotlyで使える「綺麗な２列の表」に変換する
        emo_counts = books_list['emotion'].value_counts().reset_index(name='count')
        fig = px.pie(emo_counts, names='emotion', values='count', title="読んだ本の感情割合", color_discrete_sequence=px.colors.sequential.Burgyl)
        fig_bar = px.bar(emo_counts, x='emotion', y='count', title="読んだ本の感情別統計")
        col_pie, col_bar = st.columns(2)
        with col_pie:
            st.plotly_chart(fig)
        with col_bar:
            st.plotly_chart(fig_bar)

else:
    st.info("本を登録すると、統計が表示されます！")

# 1. 新しい本の登録フォーム
st.subheader("✏️ 読んだ本を記録する")
# Google Booksから著者名を検索する機能
with st.container(border=True):
    st.write("🔍 本のタイトルから著者を自動検索（オプション）")
    search_title = st.text_input("検索したい本のタイトルを入力")

    if st.button("Google Booksで検索"):
        if search_title:
            # Google Books APIのURLを作成し、requestsでGETする
            api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{search_title}"
            res = requests.get(api_url)

            if res.status_code == 200:
                data = res.json()
                # 検索結果が存在するかチェック
                if "items" in data:
                    # 最初の検索結果(0番目)の'volumeInfo'の中にある'authors'(リスト)の最初の要素を取得
                    try:
                        fetched_author = data["items"][0]["volumeInfo"]["authors"][0]
                        fetched_title = data["items"][0]["volumeInfo"]['title']
                        st.success(f"著者が見つかりました！: {fetched_author}")
                        # 見つかった著者名をsession_stateに一時保存
                        st.session_state['auto_author'] = fetched_author
                        st.session_state['auto_title'] = fetched_title
                    except KeyError:
                        st.warning("著者のデータを見つけられませんでした...")
                else:
                    st.warning("本が見つかりませんでした...")

with st.form(key='book_form', clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        default_title = st.session_state.get("auto_title", "")
        new_title = st.text_input("本のタイトル", value=default_title)
    with col2:
        default_author = st.session_state.get("auto_author", "")
        new_author = st.text_input("著者名", default_author)

    new_rating = st.slider("評価（1~5）", min_value=1, max_value=5, value=3)
    new_review = st.text_area("感想")
    new_emotion = st.selectbox("読後の感情", emotion_list)

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
            # 保存が成功したら、一時記憶（session_state）をリセットする
            if 'auto_author' in st.session_state:
                del st.session_state['auto_author']
                del st.session_state['auto_title']
        else:
            st.error("保存に失敗しました...")
        st.rerun()

# 2. 読書ログ一覧の表示
st.markdown("---")
st.subheader("📖 これまでの読書記録")


if not books:
    st.info("まだ記録がありません。最初の本を登録してみましょう！")
else:
    col_filtered, col_all = st.columns(2)
    with col_filtered:
        st.info("フィルターを選んで読書ログを振り返りましょう！")
        filter_option = st.radio(
            "感情を選択して、フィルターをかけましょう",
            options=emotion_list,
            horizontal=True
        )
        df_filtered = books_list[books_list['emotion'] == filter_option[0]]
        if len(df_filtered) > 0:
            st.write(df_filtered)
        else:
            st.info("その感情で登録された本はありません。その感情を得られそうな本を手にとってみるのもいいかもしれません。")
    
    with col_all:
        for book in reversed(books): # 新しい記録が上に来るように、リストを逆順にする
            stars = "⭐" * book['rating'] # 評価の数だけ⭐️を表示する

            with st.container(border=True):
                col_text, col_btn = st.columns([4, 1])

                with col_text:
                    st.markdown(f"### {book['emotion']} {book['title']}")
                    st.markdown(f"**著者:** {book['author']} | **評価:** {stars}")
                    st.markdown(f"> {book['review']}")

                with col_btn:
                    if st.button("🗑️ 削除", key=f"del_{book['id']}"):
                        del_response = requests.delete(f"{API_URL}/books/{book['id']}")

                        if del_response.status_code == 200:
                            st.success(f"{book['title']}を削除しました！")
                            st.rerun()
                        else:
                            st.error("削除に失敗しました。")

                # bookの編集エリアをst.expanderを使って実装する
                with st.expander(label="✏️ 編集する"):
                    with st.form(key=f"edit_form_{book['id']}", clear_on_submit=True):
                        update_title = st.text_input(label="本のタイトル", value=f"{book['title']}")
                        update_author = st.text_input(label="著者名", value=f"{book['author']}")
                        update_rating = st.slider("評価（1~5）", min_value=1, max_value=5, value=book['rating'])
                        update_review = st.text_area("感想", value=f"{book['review']}")
                        update_emotion = st.selectbox("読後の感情を変更", ["☺️ (ほっこり)", "😂 (爆笑)", "😡 (憤り)", "☹️ (ビミョー)", "🤯 (衝撃)", "🥺 (感動)"],
                                                        key=f"emo_{book['id']}")
                        
                        submitted = st.form_submit_button("Update Book Info")

                    if submitted:
                        updated_emoji = update_emotion[0]
                        updated_payload = {"title": update_title, "author": update_author, "rating": update_rating, "review": update_review, "emotion": updated_emoji}
                        updated_response = requests.put(f"{API_URL}/books/{book['id']}", json=updated_payload)
                        if updated_response.status_code == 200:
                            st.success("Update成功")
                            st.rerun()
                        else:
                            st.error("本の編集に失敗しました...")

#else:
#    st.error("APIサーバに接続できません。バックエンドが起動しているか確認してください。")


# 学習予定メモ
#ルートB：【見栄えMAX】読書データの「可視化」ダッシュボード
#Streamlitの本当の恐ろしさ（褒め言葉）は、データ分析とグラフ描画です。
#画面のトップに、**「これまで読んだ本の感情割合（円グラフ）」や「評価分布（棒グラフ）」**を表示するダッシュボードを追加します。「自分は最近、癒やし（☺️）の本ばかり読んでるな…」といった分析ができるようになり、ポートフォリオとしての「映え」が劇的にアップします。
#
#ルートC：【技術力MAX】外部API（Google Books）との連携
#本のタイトルを入力して「検索」ボタンを押すと、自動的に「著者名」が入力される魔法のような機能を追加します。
#Pythonの requests を使って、世界中の本のデータを持つ無料の「Google Books API」と通信します。「外部APIとの連携ができる」というのは、実務においてめちゃくちゃ評価されるスキルです。