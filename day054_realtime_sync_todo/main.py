# main.py
import sqlite3
import csv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from datetime import datetime

app = FastAPI()
clients = []

conn = sqlite3.connect("todos.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT
               )
               """)
conn.commit()

@app.get("/")
async def home():
    return FileResponse("index.html")

@app.get("/export")
async def export_csv():
    # 1. データベースからすべてのタスクを取得する
    cursor.execute("SELECT title FROM tasks")
    rows = cursor.fetchall()

    # 2. CSVを書き込みモードで作成
    with open("tasks_log.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        # １行目（ヘッダー）を書き込む
        writer.writerow(["Task_Log"])
        # 取得したタスクを１行ずつ書き込む
        for row in rows:
            writer.writerow([row[0]])
    # 3. 完成したCSVをブラウザにダウンロードさせる
    return FileResponse("tasks_log.csv", filename="tasks_log.csv")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    # 1. tasksテーブルからすべてのデータ（タイトルカラム）を取得する
    cursor.execute("SELECT title FROM tasks")

    # 2. 取得したすべての行（データ）をPythonのリストとして取り出す
    rows = cursor.fetchall()

    # 3. 取得した過去のタスクを、今接続したばかりのブラウザに１つずつ送信する
    for row in rows:
        await websocket.send_text(row[0])

    try:
        while True:
            data = await websocket.receive_text()
            print("受信:", data)

            # 受け取ったデータがCLEAR_ALLなら削除処理を行う
            if data == "CLEAR_ALL":
                cursor.execute("DELETE FROM tasks")
                conn.commit()

                # ユーザに削除しましたと伝える
                for client in clients:
                    await client.send_text("CLEAR_ALL")

            # 個別削除処理
            # データが"DELETE_TASK:"から始まっていたら
            elif data.startswith("DELETE_TASK:"):
                # "DELETE_TASK:"の文字列を取り除き、タスクのテキスト部分だけを抽出
                target_text = data.replace("DELETE_TASK:", "")
                # データベースから、対象のテキストと一致するタスクを削除
                cursor.execute("DELETE FROM tasks WHERE title = ?", (target_text,))
                conn.commit()
                # 誰かが削除したら、接続している全員に同じ削除指令を転送
                for client in clients:
                    await client.send_text(data)

            # 通常のタスク追加処理
            else:
                now_time = datetime.now().strftime("%m-%d %H:%M")
                task_with_time = f"[{now_time}] {data}"
                cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task_with_time,))
                conn.commit()

                # サーバからクライアント（ブラウザ）へデータを送り返す
                for client in clients:
                    await client.send_text(task_with_time)

    except WebSocketDisconnect:
        clients.remove(websocket)