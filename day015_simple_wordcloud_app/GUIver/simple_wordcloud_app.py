#simple_wordcloud_app.py

### === Imports ===
import pandas as pd
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import flet as ft

from load_csv_gui import setup_csv_loader
from load_stopwords_gui import setup_stopwords
### === Helper Functions ===


### === App Logics ===
def main_app(page: ft.Page):
    page.title = "WordCloud Generator"


### === UI Components ===
    csv_open_button = setup_csv_loader(page)
    setup_stopwords_button = setup_stopwords(page)

### === UI Interfaces ===
    page.add(
        ft.Text("WordCloud App", size=20),
        ft.Row(csv_open_button,
        setup_stopwords_button),
    )

### === Run App ===
ft.app(target=main_app)

### === Notes ===
