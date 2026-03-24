# booklog_app.py

from fastapi import FastAPI
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI()

# 1. データの型定義
# クライアント（Streamlit）から送られてくる読書ログの「形」を定義
class BookCreate(BaseModel):
    title: str
    author: str
    rating: int = Field(ge=1, le=5, description="1 - 5の評価")
    review: str
    emotion: str

# 2. データベースの初期化
def init_db():
    conn = sqlite3.connect("reading_log.db")
    c = conn.cursor()
    # id, title, author, rating, review, emotionをすべて含めたテーブルを作成する
    c.execute('''
            CREATE TABLE IF NOT EXISTS books(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              author TEXT,
              rating INTEGER,
              review TEXT,
              emotion TEXT
              )
              ''')
    conn.commit()
    conn.close()

# 起動時にデータベースの初期化
init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to my Reading Log API!"}

# 3. 本を登録するAPI（POST）
@app.post("/books/")
def create_book(book: BookCreate):
    conn = sqlite3.connect("reading_log.db")
    c = conn.cursor()

    c.execute('''
        INSERT INTO books (title, author, rating, review, emotion)
              VALUES (?, ?, ?, ?, ?)
              ''', (book.title, book.author, book.rating, book.review, book.emotion))
    
    conn.commit()
    book_id = c.lastrowid
    conn.close()

    # Pydanticのmodel_dump()を使い、bookの中身をきれいな辞書に一発変換
    return {"id": book_id, **book.model_dump(), "status": "created"}

# 4. 本の一覧を取得するAPI
@app.get("/books/")
def read_books():
    conn = sqlite3.connect("reading_log.db")
    
    conn.row_factory = sqlite3.Row # これで列番号ではなく、列名（title, autho...）でデータを扱える！
    c = conn.cursor()

    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()

    # 辞書のリストに変換して返す（RowFactoryを使うことでシンプルに記述できるようになった）
    return [dict(row) for row in books]

# 5. 本を削除するAPI
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = sqlite3.connect("reading_log.db")
    c = conn.cursor()

    # データを削除する（SQL）
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))

    conn.commit()
    conn.close()
    return {"message": "Book deleted successfully"}

# 6. 本を更新するAPI（PUT）
@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookCreate):
    conn = sqlite3.connect("reading_log.db")
    c = conn.cursor()

    #データを更新する
    c.execute('''
        UPDATE books
              SET title=?, author=?, rating=?, review=?, emotion=?
              WHERE id = ?
              ''', (book.title, book.author, book.rating, book.review, book.emotion, book_id))
    
    conn.commit()
    conn.close()
    return {"id": book_id, **book.model_dump(), "status": "updated"}