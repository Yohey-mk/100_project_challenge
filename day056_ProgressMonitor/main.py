# main.py
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def get():
    return FileResponse("index.html")

# 重い処理（for ループ）を独立した関数として切り出す
async def run_heavy_process(websocket: WebSocket):
    try:
        for i in range(1, 101):
            await asyncio.sleep(0.05)
            await websocket.send_text(str(i))
    # キャンセル命令が飛んできた時のエラーを安全に受け止める処理
    except asyncio.CancelledError:
        print("前の処理がキャンセルされました。新しくやり直します。")
        
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    current_task = None # 現在実行中のタスクをメモしておく箱を用意する

    # 1. 何度でも合図を受け取れるように全体をwhile Trueで囲む
    try:
        while True:
            data = await websocket.receive_text()

            if data == "START":
                # もしすでにタスクが走っていたらキャンセルする
                if current_task is not None and not current_task.done():
                    current_task.cancel()
                # create_taskを使い、裏側でやっておくよう指示し、プログラムは次に進む
                current_task = asyncio.create_task(run_heavy_process(websocket))

    except WebSocketDisconnect:
        print("クライアントが切断されました")
        # ブラウザを閉じたときも処理中ならキャンセルしておく
        if current_task is not None and not current_task.done():
            current_task.cancel()
