### create_new_note.py
### Imports
import flet as ft


def user_note_input(on_submit_handler):
    note_title_field = ft.TextField(label="Title", width=300)
    note_field = ft.TextField(label="Notes", width=300, height=500)
    
    def on_submit(e):
        note = {'title':note_title_field.value, 'body':note_field.value}
        on_submit_handler(note)
        e.page.update()
        
    save_button = ft.ElevatedButton(text="Save", on_click=on_submit)
    return save_button