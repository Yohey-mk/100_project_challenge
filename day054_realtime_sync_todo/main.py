# main.py
import sqlite3
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print("受信:", data)

            cursor.execute("INSERT INTO tasks (title) VALUES (?)", (data,))
            conn.commit()

            # サーバからクライアント（ブラウザ）へデータを送り返す
            for client in clients:
                await client.send_text(data)

    except WebSocketDisconnect:
        clients.remove(websocket)