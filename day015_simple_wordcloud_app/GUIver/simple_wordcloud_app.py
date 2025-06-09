#simple_wordcloud_app.py

### === Imports ===
import pandas as pd
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import flet as ft

from load_csv_gui import setup_csv_loader, csv_text_data
from load_stopwords_gui import setup_stopwords, csv_stopwords_gui
from text_analyzer_gui import text_analyzer_gui
from gen_wordcloud import gen_wordcloud

### === Helper Functions ===
#tokens = text_analyzer_gui(csv_text_data, csv_stopwords_gui)

### === App Logics ===
def main_app(page: ft.Page):
    page.title = "WordCloud Generator"
        #dark mode <-> light mode切り替え
    theme_switch = ft.Switch(label="Dark mode", value=False)
    def toggle_theme(e):
        if theme_switch.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()
    toggle_theme(None) #アプリ起動時は初期設定（ライトモード）で起動。
    theme_switch.on_change = toggle_theme


### === UI Components ===
    csv_open_button = setup_csv_loader(page)
    setup_stopwords_button = setup_stopwords(page)
    gen_wordcloud_button = gen_wordcloud(page)

### === UI Interfaces ===
    page.add(
        ft.Text("WordCloud App", size=20),
        theme_switch,
        ft.Column(controls=[csv_open_button,
        setup_stopwords_button]),
        gen_wordcloud_button
    )

### === Run App ===
ft.app(target=main_app)

### === Notes ===
