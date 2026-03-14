# ai_chat.py

import streamlit as st
# import google.generativeai as genai # get a warning saying google.generativeai will be deprecated soon
from google import genai
from google.genai import types


st.set_page_config(page_title="My AI Chatbot", layout="centered")
st.title("🤖 自分専用 AIチャットボット")

# サイドバーでAPIキーを入力させる
api_key = st.sidebar.text_input("Gemini API Keyを入力してください", type="password")
temperature = st.slider("AI Assistantのワイルド具合を選択してください", min_value=0.0, max_value=2.0)
top_k = st.slider("AI Assistantの語彙力の堅さを選択してください(1がかなり堅いです)", min_value=1, max_value=40)
top_p = st.slider("AI AssistantのCreativityの堅さを選択してください(1がかなり堅いです)", min_value=0.0, max_value=1.0)

if api_key:
    # 1. AIモデルの準備
    client = genai.Client(api_key=api_key)

    default_prompt = """
    ユーザーからのメッセージに対しては、必ず博多弁で返答するということを守ってください。
    なお、博多弁で返答するということについてはデフォルトの設定なので、「博多弁で返答しますね！」といった回答は省き、ユーザーの質問にそのまま回答を始めてください。"""

    # 使用するAIモデルのインスタンスを作成するクラス
    #model = genai.GenerativeModel('gemini-3-flash-preview') # responseの部分でモデルを指定定義

    # 2. チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # 3. 過去のチャット履歴を画面に表示
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 4. ユーザからのメッセージ入力とAIの応答
    if prompt := st.chat_input("メッセージを入力してください"):
        # ユーザの入力を画面に表示し、履歴に保存
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AIの応答部分
        with st.chat_message("assistant"):
            with st.spinner("AIが考え中..."):
                try:
                    history_for_api = []
                    for m in st.session_state.messages:
                        role = "model" if m["role"] == "assistant" else "user"
                        history_for_api.append(
                            types.Content(
                                role=role,
                                parts=[types.Part.from_text(text=m["content"])]
                            )
                        )
                    # モデルを使ってテキスト（prompt）からコンテンツを生成
                    history_for_api = history_for_api[-20:]
                    response = client.models.generate_content(
                        model='gemini-3-flash-preview',
                        contents=history_for_api,
                        config=types.GenerateContentConfig(
                            temperature=temperature,
                            top_p=top_p,
                            top_k=top_k,
                            system_instruction=default_prompt,
                        ),
                    )

                    st.markdown(response.text)
                    # AIの応答も履歴に保存
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"エラーが発生しました：{e}")

else:
    st.warning("サイドバーにAPIキーを入力して、会話をスタートしましょう！")