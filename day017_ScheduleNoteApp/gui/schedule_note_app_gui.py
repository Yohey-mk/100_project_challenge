# schedule_note_app_gui.py

### === Imports ===
import flet as ft
#import os

from save_notebook import save_notebook, load_notebook
#from add_schedule import add_schedule
from back_home import back_home
#from show_all_notes import show_all_notes
#from show_schedule import show_schedule
#from edit_schedule import edit_schedule
### === Helper Functions ===


### === App Logics ===
def main(page: ft.Page):
    page.title = "Schedule Note App"
#    page.scroll = "auto"
    my_schedule = load_notebook()
#    home_button = ft.ElevatedButton("HOME", on_click=lambda e: back_home(page, on_submit_handler))

#最初にsave_shedule()を作成する。※裏側でworkするモジュール。
    def on_submit_handler(schedule):
        my_schedule.append(schedule)
        save_notebook(my_schedule)
        page.snack_bar = ft.SnackBar(ft.Text("Schedule added!"))
        page.snack_bar.open = True
        page.update()

    back_home(page, my_schedule, on_submit_handler)
#    def call_add_schedule(e):
#        page.controls.clear()
#        page.controls.append(add_schedule(on_submit_handler))
#        page.controls.append(home_button)
#        page.update()

#    def call_show_schedule(e):
#        page.controls.clear()
#        page.controls.append(show_schedule(page, my_schedule))
#        page.controls.append(home_button)
#        page.update()

#    def call_show_all_notes(e):
#        page.controls.clear()
#        page.controls.append(show_all_notes(page, my_schedule))
#        page.controls.append(home_button)
#        page.update()

#    def call_edit_schedule(e):
#        page.controls.clear()
#        page.controls.append(edit_schedule(page, my_schedule))
#        page.controls.append(home_button)
#        page.update()

#    def quit_app(e):
#        os._exit(0)

### === UI Components ===
#    call_add_schedule_ui = ft.ElevatedButton("Add Schedule", on_click=call_add_schedule)
#    show_schedule_ui = ft.ElevatedButton("Show Schedule", on_click=call_show_schedule)
#    show_details_ui = ft.ElevatedButton("Show Details", on_click=call_show_all_notes)
#    edit_schedule_ui = ft.ElevatedButton("Edit Schedule", on_click=call_edit_schedule)
#    quit_app_ui = ft.ElevatedButton("Quit App", on_click=quit_app)

### === UI Interfaces ===
#    page.add(
#        call_add_schedule_ui,
#        show_schedule_ui,
#        show_details_ui,
#        edit_schedule_ui,
#        quit_app_ui
#    )

### === Run App ===
ft.app(target=main)


### === Notes ===
# ✅ 最終的な目標（ステップの先に…）
#	•	タスクの並び替え（ドラッグ＆ドロップ）
#	•	フィルタ機能（特定の日付のみ表示など）
#	•	ダークモード対応
#	•	“常に最前面” トグル（前に話していた要件！）
