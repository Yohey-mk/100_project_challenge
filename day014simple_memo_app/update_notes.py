#update_notes.py
### === Imports ===
import flet as ft
from save_notebook import save_notebook

### === Functions ===
def update_notes(page:ft.Page, my_notebook, display_column):
    choose_note = ft.TextField(label="Enter note # to update")
    title_field = ft.TextField(label="Title")
    content_field = ft.TextField(label="Content")

    #Cardsでメモを表示する
    note_cards = ft.Column()
    for idx, note in enumerate(my_notebook):
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{idx + 1}. {note['title']}", weight="bold"),
                    ft.Text(note['body']),
                ]),
                padding=10,
            )
        )
        note_cards.controls.append(card)

    #Cardsのリフレッシュ
    def refresh_note_cards():
        note_cards.controls.clear()
        for idx, note in enumerate(my_notebook):
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"{idx + 1}. {note['title']}", weight="bold"),
                        ft.Text(note['body'])
                    ]),
                    padding=10,
                )
            )
            note_cards.controls.append(card)
        page.update()

    def load_note(e):
        try:
            idx = int(choose_note.value) - 1
            if 0 <= idx < len(my_notebook):
                note = my_notebook[idx]
                title_field.value = note["title"]
                content_field.value = note["body"]
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Invalid note number"))
                page.snack_bar.open = True
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Enter a valid number"))
            page.snack_bar.open = True
        page.update()

    def save_updated_note(e):
        idx = int(choose_note.value) - 1
        if 0 <= idx < len(my_notebook):
            my_notebook[idx] = {
                "title": title_field.value,
                "body": content_field.value
            }
            save_notebook(my_notebook)
            refresh_note_cards()
            page.snack_bar = ft.SnackBar(ft.Text("Note updated successfully!"))
            page.snack_bar.open = True
            page.update()

    load_button = ft.ElevatedButton(text="Load", on_click=load_note)
    save_button = ft.ElevatedButton(text="Save", on_click=save_updated_note)


    return ft.Column([
        ft.Text("Select a note to update"),
        choose_note,
        load_button,
        title_field,
        content_field,
        save_button,
        ft.Text("Current Notes", style="headlineSmall"),
        note_cards])
    #return ft.Text("This is a debug section.")