#update_notes.py
### === Imports ===
import flet as ft

### === Functions ===
def update_notes(page:ft.Page, my_notebook, display_column, show_all_notes):
    show_note_cards = ft.ElevatedButton(text="Show Notes",on_click=show_all_notes)
    def on_click(e):
        page.controls.clear()
        choose_note = ft.TextField(label="Enter note # to update")
        page.add(
            ft.Text("All cleared."),
            choose_note,
            show_note_cards
        )
        page.update()
    update_button = ft.ElevatedButton(text="Update", on_click=on_click)
    return ft.Column([update_button, show_note_cards])
    #return ft.Text("This is a debug section.")