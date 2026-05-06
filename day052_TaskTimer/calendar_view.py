# calendar_view.py

### Imports
import calendar
from datetime import datetime
import flet as ft

### Main Logic

def render_calendar_ui(page: ft.Page, year: int, month: int, on_back_callback):
    page.controls.clear()

    title = ft.Text(f"{year}年 {month}月", size=20, weight="bold")

    def change_month(page: ft.Page, year: int, month: int, delta: int):
        month += delta
        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1
        render_calendar_ui(page, year, month, on_back_callback)

    previous_btn = ft.Button(
        content="◀",
        on_click=lambda e: change_month(page, year, month, -1)
    )
    next_btn = ft.Button(
        content="▶",
        on_click=lambda e: change_month(page, year, month, 1)
    )

    change_month_ui = ft.Row(
        controls=[previous_btn, title, next_btn],
        alignment=ft.Alignment.CENTER,
        spacing=20
    )

    CELL_WIDTH = 60

    weekday_labels = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    weekdays = [
        ft.Container(
            content=ft.Text(day, text_align='CENTER'),
            width=CELL_WIDTH,
            alignment=ft.Alignment.CENTER
        )
        for day in weekday_labels
    ]
    weekday_row = ft.Row(controls=weekdays, alignment=ft.Alignment.CENTER)

    weeks = calendar.Calendar(firstweekday=calendar.SUNDAY).monthdayscalendar(year, month)
    calendar_rows = []

    for week in weeks:
        row = []
        for day in week:
            if day == 0:
                row.append(ft.Container(width=CELL_WIDTH))
            else:
                row.append(
                    ft.Button(
                        content=str(day),
                        width=CELL_WIDTH,
                        on_click=lambda e: None
                    )
                )
        calendar_rows.append(ft.Row(controls=row, alignment=ft.Alignment.CENTER))

    home_button=ft.Button(content="HOME", on_click=on_back_callback)
    home_button_ui = ft.Row(controls=[home_button], alignment=ft.Alignment.CENTER)
    
    page.add(
        change_month_ui,
        weekday_row,
        *calendar_rows,
        home_button_ui
    )
    page.update()

