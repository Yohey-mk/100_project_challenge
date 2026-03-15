# task_api.py

from fastapi import FastAPI
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI()

# データベースの初期化
def init_db():
    conn = sqlite3.connect("api_tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT)''')
    conn.commit()
    conn.close()

init_db()

# データの型定義
# クライアント（Streamlitやスマホアプリなど）から送られてくるデータの「形」を厳密に定義します
class TaskCreate(BaseModel):
    title: str
    description: str | None = Field(default=None, title="Description", max_length=200)

# APIエンドポイント（ここからがAPIの窓口）
# データを取得するGETメソッドで、ルートパス("/")にアクセスしたときの処理を定義するデコレータ
@app.get("/")
def read_root():
    return {"message": "Welcome to my Task API!"}

@app.post("/tasks/")
def create_task(task: TaskCreate):
    conn = sqlite3.connect("api_tasks.db")
    c = conn.cursor()
    c.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (task.title, task.description,))
    conn.commit()
    task_id = c.lastrowid
    conn.close()
    return {"id": task_id, "title": task.title, "description": task.description, "status": "created"}

@app.get("/tasks/")
def read_tasks():
    conn = sqlite3.connect("api_tasks.db")
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()

    return [{"id": row[0], "title":row[1], "desc":row[2]} for row in tasks]

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    conn = sqlite3.connect("api_tasks.db")
    c = conn.cursor()
    c.execute('''
        UPDATE tasks
        SET title = ?, description = ?
        WHERE id = ?
        ''', (task.title, task.description, task_id))
    conn.commit()
    conn.close()

    return {"id": task_id, "title": task.title, "description": task.description, "status": "updated"}