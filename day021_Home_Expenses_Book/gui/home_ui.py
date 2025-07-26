# home_ui.py

### === Imports ===
import flet as ft
from datetime import datetime
from utils import on_save_clicked
from calendar_view import render_calendar_ui, open_day_editor

### Main Logic
def back_home(page: ft.Page):
    page.controls.clear()
    
    page.scroll = "auto"

    ### UI Components
    home_button = ft.ElevatedButton(text="HOME", on_click=lambda e:back_home(page))
    #date_input_button = ft.ElevatedButton("Input", on_click=lambda e:on_save_clicked(e))
    calendar_view_button = ft.ElevatedButton(
        text="Calendar",
        on_click=lambda e: render_calendar_ui(page, datetime.now().year, datetime.now().month))
    
    home_button_ui = ft.Row(controls=[home_button], alignment="center")
    calendar_view_button_ui = ft.Row(controls=[calendar_view_button], alignment="center")

    show_today_editor = ft.ElevatedButton(text="TODAY", on_click=lambda e: open_day_editor(page, datetime.now().year, datetime.now().month, datetime.now().day))
    show_today_editor_ui = ft.Row(controls=[show_today_editor], alignment="center")

    page.add(
        home_button_ui,
        calendar_view_button_ui,
        show_today_editor_ui
        #date_input_button
    )
    page.update()