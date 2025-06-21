# schedule_note_app_gui.py

### === Imports ===
import flet as ft

### === Helper Functions ===


### === App Logics ===
def main(page: ft.Page):
    page.title = "Schedule Note App"

    def add_schedule(e):
        pass

    def show_schedule(e):
        pass

    def show_all_notes(e):
        pass

    def edit_schedule(e):
        pass

    def quit_app(e):
        pass

### === UI Components ===


### === UI Interfaces ===
    page.add(
        ft.ElevatedButton("Add Schedule", on_click=add_schedule),
        ft.ElevatedButton("Show Schedule", on_click=show_schedule),
        ft.ElevatedButton("Show Details", on_click=show_all_notes),
        ft.ElevatedButton("Edit Schedule", on_click=edit_schedule),
        ft.ElevatedButton("Quit App", on_click=quit_app)
    )

### === Run App ===
ft.app(target=main)