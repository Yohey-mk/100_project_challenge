### create_new_note.py
### Imports
import flet as ft


def user_note_input(on_submit_handler):
    note_field = ft.TextField(label="Notes", width=300, height=500)
    
    def on_submit(e):
        note_to_add = note_field.value
        on_submit_handler(note_to_add)
        e.page.update()
        
    save_button = ft.ElevatedButton(text="Save", on_click=on_submit)