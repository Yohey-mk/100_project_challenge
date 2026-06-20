# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()

# 現在のタスクの状態（最初は未着手）
current_state = "NOT_STARTED"

# 許可されている状態繊維のルールブックを辞書型で定義
# 今の状態 -> 次に移動できる状態 のリスト
ALLOWED_TRANSITIONS = {
    "NOT_STARTED": ["RUNNING"],
    "RUNNING": ["PAUSED", "FINISHED"],
    "PAUSED": ["RUNNING", "FINISHED"],
    "FINISHED": [] # 完了したらどこにも遷移できなくする
}

@app.get("/")
async def get():
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global current_state
    await websocket.accept()

    # ブラウザが開いたら、まずは現在の状態を教える
    await websocket.send_text(f"STATE:{current_state}")

    try:
        while True:
            # ブラウザから状態リクエストを受信する
            action = await websocket.receive_text()

            # バックエンドで送られてきたactionが現在の状態から移動できるリストに入っているか確認
            if action in ALLOWED_TRANSITIONS[current_state]:
                current_state = action
                await websocket.send_text(f"STATE:{current_state}")
            else:
                # ルール上進めない場合はエラーメッセージを返す
                await websocket.send_text(f"ERROR: {current_state} -> {action}には進めません")
    except WebSocketDisconnect:
        pass