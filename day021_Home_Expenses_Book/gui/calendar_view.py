# calendar_view.py

### Imports
import calendar
from datetime import date
import flet as ft

from utils import save_csv, load_csv

def render_calendar_ui(page: ft.Page, year: int, month: int):
    page.controls.clear()

    title = ft.Text(f"{year}年 {month}月", size=24, weight="bold")

    weekday_labels = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    weekdays = [ft.Text(day, text_align="center") for day in weekday_labels]

    cal = calendar.Calendar()
    days = cal.itermonthdates(year, month)

    grid_items = []
    for day in days:
        if day == 0:
            grid_items.append(ft.Container())
        else:
            btn = ft.ElevatedButton(
                text=str(day),
                on_click=lambda e, d=day: open_day_editor(page, year, month, d)
            )
            grid_items.append(btn)

    page.add(
        title,
        ft.Row(controls=weekdays, alignment="spaceAround"),
        ft.GridView(
            runs_count=7,
            max_extent=80,
            controls=grid_items,
            expand=True
        )
    )
    page.update()


def open_day_editor(page: ft.Page, year: int, month: int, day: int):
    page.controls.clear()

    selected_date = f"{year:04d}-{month:02d}-{day:02d}"
    date_label = ft.Text(f"Records: {selected_date}", size=20)

    category = ft.TextField(label="Category")
    amount = ft.TextField(label="Amount")
    memo = ft.TextField(label="Memo")

    def on_save(e):
        save_csv_entry(selected_date, category.value, amount.value, memo.value)
        page.controls.append(ft.Text("Saved!"))
        page.update()

    save_button = ft.ElevatedButton("Save", on_click=on_save)
    back_button = ft.ElevatedButton("Back", on_click=lambda e: render_calendar_ui(page, year, month))

    page.add(
        date_label,
        category,
        amount,
        memo,
        ft.Row([save_button, back_button])
    )
    page.update()


def save_csv_entry(date_str, category, amount, memo, filename="day21_gui.csv"):
    df = load_csv(filename)
    new_row = {
        "Date": date_str,
        "Category": category,
        "Amount": int(amount),
        "Memo": memo
    }
    df.loc[len(df)] = new_row
    save_csv(df, filename)