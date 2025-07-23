# home_ui.py

### === Imports ===
import flet as ft
from utils import on_save_clicked


### Main Logic
def back_home(page: ft.Page):
    page.controls.clear()
    
    page.scroll = "auto"

    on_save_clicked(page)


    ### UI Components
    home_button = ft.ElevatedButton(text="HOME", on_click=lambda e:back_home(page))

    page.add(
        home_button,
    )
    page.update()