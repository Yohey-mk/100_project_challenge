# back_home.py
import flet as ft
import os
from add_schedule import add_schedule
from edit_schedule import edit_schedule
from show_all_notes import show_all_notes
from show_schedule import show_schedule
#from save_notebook import load_notebook

def back_home(page: ft.Page, my_schedule: list, on_submit_handler):
    page.controls.clear()
    #my_schedule = load_notebook()
    home_button = ft.ElevatedButton("HOME", on_click=lambda e: back_home(page, my_schedule, on_submit_handler))
    page.scroll = "auto"

    def call_add_schedule(e):
        page.controls.clear()
        page.controls.append(add_schedule(on_submit_handler))
        page.controls.append(home_button)
        page.update()

    def call_show_schedule(e):
        page.controls.clear()
        page.controls.append(show_schedule(page, my_schedule))
        page.controls.append(home_button)
        page.update()

    def call_show_all_notes(e):
        page.controls.clear()
        page.controls.append(show_all_notes(page, my_schedule))
        page.controls.append(home_button)
        page.update()

    def call_edit_schedule(e):
        page.controls.clear()
        page.controls.append(edit_schedule(page, my_schedule))
        page.controls.append(home_button)
        page.update()

    def quit_app(e):
        os._exit(0)

    ### === UI Components ===
    call_add_schedule_ui = ft.ElevatedButton("Add Schedule", on_click=call_add_schedule)
    show_schedule_ui = ft.ElevatedButton("Show Schedule", on_click=call_show_schedule)
    show_details_ui = ft.ElevatedButton("Show Details", on_click=call_show_all_notes)
    edit_schedule_ui = ft.ElevatedButton("Edit Schedule", on_click=call_edit_schedule)
    quit_app_ui = ft.ElevatedButton("Quit App", on_click=quit_app)
    page.add(
        call_add_schedule_ui,
        show_schedule_ui,
        show_details_ui,
        edit_schedule_ui,
        quit_app_ui
    )
    page.update()