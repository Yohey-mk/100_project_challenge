#Show all notes.py
### === Imports ===
import flet as ft

### === Functions ===
def show_all_notes(page, my_notebook,display_column):
    try:
        display_column.controls.clear()
        for idx, entry in enumerate(my_notebook):
            display_column.controls.append(
                ft.Text(f"{idx + 1}: {entry['title']}")
            )
        page.update()
        return display_column
    except Exception as e:
        return ft.Text(f"Error displaying notes: {e}")