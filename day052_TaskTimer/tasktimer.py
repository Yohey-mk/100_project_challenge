# tasktimer.py

import flet as ft

def main(page: ft.Page):
    page.title = "TaskTracker"
    page.scroll = "auto"
    page.window.width = 300
    page.window.height = 400
    page.window.always_on_top = True


    # Layout
    msg = ft.Text("Welcome to Task Tracker!")

    # Page.add
    page.add(
        ft.Row(
            msg,
        )
    )

ft.run(main)