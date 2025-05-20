### Day14: simple_memo_app.py

### === Imports ===
import flet as ft
from create_new_note import user_note_input
from show_all_notes import show_all_notes
from update_notes import update_notes
from save_notebook import save_notebook,resource_path,load_notebook
from delete_notes import delete_notes

### === Helper Functions ===


### === App Logics ===
def main(page: ft.Page):
    page.scroll = "auto"
    page.window.resizable = True
    page.title = "Simple Notepad"

    my_notebook = load_notebook()


    def on_submit_handler(user_note_input):
        my_notebook.append(user_note_input)
        save_notebook(my_notebook)

### === UI Components ===


### === UI Interface ===


### === Run App ===








#notes
#✨️✨️✨️Always on top機能を実装してみる？今後の練習として！✨️✨️✨️
#⸻
#
#⭐ GUIで追加する機能の例（Fletで挑戦）
#	•	入力欄＋保存ボタン
#	•	メモ一覧をリスト表示（ListView）
#	•	タイトルをクリックすると内容を読み込み・編集できる
#	•	保存・削除ボタン
#	•	アプリを閉じてもメモが保持される（JSONによる永続化）

#JSON構造のヒント
#[
#  {
#    "title": "買い物リスト",
#    "content": "卵、牛乳、バナナ"
#  },
#  {
#    "title": "打ち合わせメモ",
#    "content": "水曜10時 Zoomリンク: ..."
#  }
#]
