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

    def create_new_note(e):
        note_title_field.value = ""
        note_field.value = ""
        e.page.update()
        
    save_button = ft.ElevatedButton(text="Save as new note", on_click=on_submit)
    create_new_note_button = ft.ElevatedButton(text="Create New", on_click=create_new_note)
    return ft.Column(controls=[note_title_field,note_field,save_button,create_new_note_button])
