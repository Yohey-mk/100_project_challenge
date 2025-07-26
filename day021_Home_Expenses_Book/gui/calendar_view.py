# calendar_view.py

### Imports
import calendar
from datetime import date
import flet as ft

from utils import save_csv, load_csv
#from home_ui import back_home

def go_back(page: ft.Page):
    import home_ui
    home_ui.back_home(page)

def render_calendar_ui(page: ft.Page, year: int, month: int):
    page.controls.clear()

    title = ft.Text(f"{year}年 {month}月", size=24, weight="bold")

    previous_btn = ft.ElevatedButton(
        text="◀",
        on_click=lambda e: change_month(page, year, month, -1)
    )
    next_btn = ft.ElevatedButton(
        text="▶",
        on_click=lambda e: change_month(page, year, month, 1)
    )

    def change_month(page: ft.Page, year: int, month: int, delta: int):
        month += delta
        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1
        render_calendar_ui(page, year, month)

    change_month_ui = ft.Row(
        controls=[previous_btn, title, next_btn],
        alignment="center",
        spacing=20
    )

    CELL_WIDTH = 60

    weekday_labels = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    weekdays = [
        ft.Container(
            content=ft.Text(day, text_align="center"),
            width=CELL_WIDTH,
            alignment=ft.alignment.center
        )
        for day in weekday_labels
    ]
    weekday_row = ft.Row(controls=weekdays, alignment="center")

    #cal = calendar.Calendar()

    weeks = calendar.Calendar().monthdayscalendar(year, month)
    calendar_rows = []

    for week in weeks:
        row = []
        for day in week:
            if day == 0:
                row.append(ft.Container(width=CELL_WIDTH))
            else:
                row.append(
                    ft.ElevatedButton(
                        text=str(day),
                        width=CELL_WIDTH,
                        on_click=lambda e, d=day: open_day_editor(page, year, month, d)
                    )
                )
        calendar_rows.append(ft.Row(controls=row, alignment="center"))

    home_button=ft.ElevatedButton(text="HOME", on_click=lambda e:go_back(page))
    home_button_ui = ft.Row(controls=[home_button], alignment="center")
    
    page.add(
        change_month_ui,
        weekday_row,
        *calendar_rows,
        home_button_ui
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
        try:
            save_csv_entry(selected_date, category.value, amount.value, memo.value)
            page.controls.append(ft.Text("Saved!"))
        except ValueError:
            page.controls.append(ft.Text("Amount must be a number.", color="red"))
        page.update()

    save_button = ft.ElevatedButton("Save", on_click=on_save)
    back_button = ft.ElevatedButton("Back", on_click=lambda e: render_calendar_ui(page, year, month))

    def show_other_notes(e, filename="day21_gui.csv"):
        notebook = load_csv(filename)
        filtered_notebook = notebook[notebook["Date"] == selected_date]
        schedule_list = ft.Column()
        
        def refresh_notebook_list():
            schedule_list.controls.clear()
            for idx, (_, schedule) in enumerate(filtered_notebook.iterrows()):
                item = ft.Column([
                    ft.Text(f"#{idx + 1}. {schedule['Category']}"),
                    ft.Text(f"{schedule['Amount']}"),
                    ft.Text(f"{schedule['Memo']}")
                ])
                schedule_list.controls.append(item)
            page.update()

        refresh_notebook_list()
        page.controls.append(schedule_list)
        page.update()

    show_notes_by_date_btn = ft.ElevatedButton(text="Show Other Notes", on_click=show_other_notes)

    page.add(
        date_label,
        category,
        amount,
        memo,
        ft.Row([save_button, back_button]),
        ft.Divider(),
        show_notes_by_date_btn
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