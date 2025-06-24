# schedule_note_app_gui.py

### === Imports ===
import flet as ft
import os

from save_notebook import save_notebook, load_notebook
from add_schedule import add_schedule
### === Helper Functions ===


### === App Logics ===
def main(page: ft.Page):
    page.title = "Schedule Note App"

    my_schedule = load_notebook()

#最初にsave_shedule()を作成する。※裏側でworkするモジュール。
    def on_submit_handler(schedule):
        my_schedule.append(schedule)
        save_notebook(my_schedule)
        page.snack_bar = ft.SnackBar(ft.Text("Schedule added!"))
        page.update()
    def call_add_schedule(e):
        page.controls.clear()

    def call_show_schedule(e):
        pass

    def call_show_all_notes(e):
        pass

    def call_edit_schedule(e):
        pass

    def quit_app(e):
        os._exit(0)

### === UI Components ===
    add_schedule_ui = add_schedule(on_submit_handler)
    show_schedule_ui = ft.ElevatedButton("Show Schedule", on_click=call_show_schedule)
    show_details_ui = ft.ElevatedButton("Show Details", on_click=call_show_all_notes)
    edit_schedule_ui = ft.ElevatedButton("Edit Schedule", on_click=call_edit_schedule)
    quit_app_ui = ft.ElevatedButton("Quit App", on_click=quit_app)

### === UI Interfaces ===
    page.add(
        add_schedule_ui,
        show_schedule_ui,
        show_details_ui,
        edit_schedule_ui,
        quit_app_ui
    )

### === Run App ===
ft.app(target=main)


### === Notes ===
# ✅ 最終的な目標（ステップの先に…）
#	•	タスクの並び替え（ドラッグ＆ドロップ）
#	•	フィルタ機能（特定の日付のみ表示など）
#	•	ダークモード対応
#	•	“常に最前面” トグル（前に話していた要件！）
