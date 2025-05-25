# === Imports ===
import flet as ft

#expense_display = ft.Column()

def show_current_list(expense_book, display_column):
    display_column.controls.clear()
    for idx, entry in enumerate(expense_book):
        display_column.controls.append(
            ft.Text(f"{idx + 1}: {entry['date']} - {entry['item']}: JPY{entry['expense']}")
        )