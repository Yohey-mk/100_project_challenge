# home_expenses_book_cli.py

### === Imports ===
import pandas as pd
import csv
import sys
import os

from add_expenses import add_expenses
from show_list import show_list
from edit_utils import edit_list
from utils import load_csv, save_csv, get_valid_date

### === Helper Sub-Functions ===


### === Helper Functions ===
def quit_app():
    exit()

### === App Logics ===
def main():
    df = load_csv()
    while True:
        print("\n家計簿メニュー")
        print("1. 出費を追加")
        print("2. 出費を表示")
        print("3. 出費を編集")
        print("4. アプリを終了")
        choice = input("選択肢を入力してください(1~4): ")

        if choice == "1":
            date = get_valid_date()
            df = add_expenses(df, date)
            save_csv(df)
        elif choice == "2":
            show_list(df)
        elif choice == "3":
            edit_list(df)
            save_csv(df)
        elif choice == "4":
            save_csv(df)
            quit_app()
        else:
            print("無効な選択肢です。")

### === Run App ===
if __name__ == "__main__":
    main()


# notes
# 前回より進化を目指すには？
# カレンダー機能をつけたい。具体的には、カレンダー表示にその日の出費を表示させる＆Addできる。
# ↑はGUI版での機能なので、CLI版では省略
# したがって、GUI版はインターフェースをカレンダーベースにする。イメージとしては、手帳の月または週表示。
