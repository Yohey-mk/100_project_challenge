# === Imports ===
import flet as ft

def update_choice(refresh_display,expense_book, page):
    user_input_field = ft.TextField(label="Select item # to modify", width=300)

    date_input_field = ft.TextField(label="New Date")
    item_input_field = ft.TextField(label="New Item")
    expense_input_field = ft.TextField(label="New Expense")

    def on_click(e):
        try:
            user_selected_index = int(user_input_field.value) - 1
            selected_entry = expense_book[user_selected_index]
            date_input_field.value = selected_entry["date"]
            item_input_field.value = selected_entry["item"]
            expense_input_field.value = selected_entry["expense"]
            page.update()

        except (ValueError, IndexError):
            page.snack_bar = ft.SnackBar(ft.Text("Invalid selection"), open=True)
            page.update()

    def on_submit_update(e):
        try:
            user_selected_index = int(user_input_field.value) - 1
            expense_book[user_selected_index] = {
                "date": date_input_field.value,
                "item": item_input_field.value,
                "expense": int(expense_input_field.value)
            }
            refresh_display()
            page.snack_bar = ft.SnackBar(ft.Text("Entry Updated!"), open=True)
            page.update()

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), open=True)
            page.update()
    return ft.Column(
        controls=[
            user_input_field,
            ft.ElevatedButton("Select", on_click=on_click),
            date_input_field,
            item_input_field,
            expense_input_field,
            ft.ElevatedButton("Save Update", on_click=on_submit_update)
        ]
    )



