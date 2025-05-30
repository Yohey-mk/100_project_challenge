#delete_notes.py
### === Imports ===
import flet as ft
from save_notebook import save_notebook

### === Functions ===
def delete_notes(page:ft.Page, my_notebook, display_column):
    choose_note = ft.TextField(label="Enter note # to delete")
    title_field = ft.TextField(label="Title")
    content_field = ft.TextField(label="Content")

    note_cards = ft.Column()
    for idx, note in enumerate(my_notebook):
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{idx + 1}. {note['title']}", weight="bold"),
                    ft.Text(f"{note['body']}"),
                ]),
                padding=10
            )
        )
        note_cards.controls.append(card)

    # Card一覧のリフレッシュ
    def refresh_cards():
        note_cards.controls.clear()
        for idx, note in enumerate(my_notebook):
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"{idx + 1}. {note['title']}", weight="bold"),
                        ft.Text(f"{note['body']}"),
                    ]),
                    padding=10,
                )
            )
            note_cards.controls.append(card)
        page.update()

    def load_notes(e):
        try:
            idx = int(choose_note.value) - 1
            if 0 <= idx < len(my_notebook):
                note = my_notebook[idx]
                title_field.value = note['title']
                content_field.value = note['body']
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Invalid input"))
                page.snack_bar.open = True
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Enter a valid number"))
            page.snack_bar.open = True
        page.update()

    def pop_notes(e):
        try:
            idx = int(choose_note.value) - 1
            if 0 <= idx < len(my_notebook):
                my_notebook.pop(idx)
                save_notebook(my_notebook)
                choose_note.value = ""
                title_field.value = ""
                content_field.value = ""
                refresh_cards()
                page.snack_bar = ft.SnackBar(ft.Text("Note deleted!"))
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Invalid input"))
                page.snack_bar.open = True
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Enter a valid number"))
            page.snack_bar.open = True
            page.update()

    load_button = ft.ElevatedButton(text="Load", on_click=load_notes)
    delete_button = ft.ElevatedButton(text="Delete", on_click=pop_notes)

    return ft.Column([
        ft.Text("First, hit the load button to show notes"),
        choose_note,
        load_button,
        title_field,
        content_field,
        delete_button,
        ft.Text("Current notes"),
        note_cards
    ])