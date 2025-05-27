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
    display_column = ft.Column()


    def on_submit_handler(note):
        title = note["title"]

        for i, existing_note in enumerate(my_notebook):
            if existing_note["title"] == title:
                my_notebook[i] = note
                break
        else:
            my_notebook.append(note)
        save_notebook(my_notebook)
        page.snack_bar = ft.SnackBar(ft.Text("Notes Added!"))
        page.snack_bar.open = True
        page.update()

    def call_update_page(e):
        page.controls.clear()
        update_ui = update_notes(page, my_notebook, display_column)
        page.add(update_ui, home_button_ui)
        page.update()

    def home_button(e):#button -> on_click -> show all ui (again)という構造にすれば、擬似的にホーム回帰を再現可能？
        page.controls.clear()
        page.add(
            create_note_ui,
            update_notes_ui,
            show_notes_ui,
            home_button_ui
        )
        page.update()

### === UI Components ===
    create_note_ui = user_note_input(on_submit_handler)
    update_notes_ui = ft.ElevatedButton(text="Update", on_click=call_update_page)
    show_notes_ui = show_all_notes(page, my_notebook, display_column)
    home_button_ui = ft.ElevatedButton(text="HOME",on_click=home_button)

### === UI Interface ===
    page.add(
        create_note_ui,
        update_notes_ui,
        show_notes_ui,
        home_button_ui,
    )

### === Run App ===
ft.app(target=main)







#notes
#✨️✨️✨️Always on top機能を実装してみる？今後の練習として！✨️✨️✨️
#5.27 Update自体はOK,Update→Updateした情報で画面の更新＆ホームボタンの設置でホーム画面に戻れるように設計
#Next Step -> Delete機能の追加、基本的な構造はUpdate_notesを参考にすればできそう？Card表示とか。Delete機能が完成したら、Day14は一旦完成！
#
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
