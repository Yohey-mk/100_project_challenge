# schedule_note_app_gui.py

### === Imports ===
import flet as ft

from save_notebook import save_notebook
from add_schedule import add_schedule
### === Helper Functions ===


### === App Logics ===
def main(page: ft.Page):
    page.title = "Schedule Note App"
#最初にsave_shedule()を作成する。※裏側でworkするモジュール。
    def call_add_schedule(e):
        page.controls.clear()

    def call_show_schedule(e):
        pass

    def call_show_all_notes(e):
        pass

    def call_edit_schedule(e):
        pass

    def quit_app(e):
        pass

### === UI Components ===


### === UI Interfaces ===
    page.add(
        ft.ElevatedButton("Add Schedule", on_click=add_schedule),
        ft.ElevatedButton("Show Schedule", on_click=call_show_schedule),
        ft.ElevatedButton("Show Details", on_click=call_show_all_notes),
        ft.ElevatedButton("Edit Schedule", on_click=call_edit_schedule),
        ft.ElevatedButton("Quit App", on_click=quit_app)
    )

### === Run App ===
ft.app(target=main)


### === Notes ===
# ✅ 最終的な目標（ステップの先に…）
#	•	タスクの並び替え（ドラッグ＆ドロップ）
#	•	フィルタ機能（特定の日付のみ表示など）
#	•	ダークモード対応
#	•	“常に最前面” トグル（前に話していた要件！）
