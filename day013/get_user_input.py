# === Imports ===
import flet as ft

# === Helper Functions ===
def get_user_input(on_submit_handler):
    date_field = ft.TextField(
        label="Enter a date (yyyy-mm-dd)",
        hint_text="2025-01-01",
        width=300
    )
    item_field = ft.TextField(
        label="Enter item name",
        hint_text="Coffee, Lunch, etc.",
        width=300
    )
    expense_field = ft. TextField(
        label="Enter expense (JPY)",
        hint_text="1000",
        width=300
    )

    def on_click(e):
        data = {
            "date": date_field.value,
            "item": item_field.value,
            "expense": expense_field.value
        }
        on_submit_handler(data)
        #入力欄をクリアにする
        date_field.value = ""
        item_field.value = ""
        expense_field.value = ""
        e.page.update()

    submit_button = ft.ElevatedButton(
        text="Submit",
        on_click=on_click
    )
    return ft.Column(
        controls=[date_field, item_field, expense_field, submit_button]
    )