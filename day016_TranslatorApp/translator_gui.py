#translator_gui.py

### === Imports ===
import flet as ft
from argostranslate import translate
from translation_handler import translation_handler_ui

### === App Logics ===
def main(page: ft.Page):
    page.title = "Simple EN -> JP Translator"

### === UI Interfaces ===
    page.add(translation_handler_ui())

### === Run App ===
ft.app(target=main)