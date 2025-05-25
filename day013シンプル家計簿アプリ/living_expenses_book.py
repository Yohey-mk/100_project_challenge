#Day13: シンプル家計簿アプリ（CLI → GUI）
# === Imports ===
import flet as ft
import os
from get_user_input import get_user_input
from show_updated_list import show_current_list
from update_list import update_choice
#from quit_app import quit_app
from storage import save_data, load_data

# === Helper Functions ===


# === App Logics ===
def main(page: ft.Page):
    page.window_width = 300
    page.window_height = 700
    page.scroll = "auto"
    page.window_resizable = True

    page.title = "Living Expense Book"

    expense_book = load_data()
    expense_display = ft.Column()
    total_text = ft.Text("Total: JPY0")

# === UI Components ===
    def on_submit_handler(user_input_data):
        try:
            user_input_data["expense"] = int(user_input_data["expense"])
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid expense input!"), open=True)
            page.update()
            return

        expense_book.append(user_input_data)
        save_data(expense_book)
        refresh_display()
        #show_current_list(expense_book, expense_display)

        page.snack_bar = ft.SnackBar(ft.Text("Data submitted!"))
        page.snack_bar.open = True
        page.update()

    user_input_ui =get_user_input(on_submit_handler)

    #show_current_list
    def refresh_display():
        show_current_list(expense_book, expense_display)
        total = sum(entry['expense'] for entry in expense_book)
        total_text.value = f"Total: JPY{total}"
        save_data(expense_book)
        page.update()

    #update_list
    update_list_ui = update_choice(refresh_display,expense_book, page)

    #quit_app
    def on_quit(e):
        save_data(expense_book)
        os._exit(0)
    exit_app = (ft.ElevatedButton(text="QUIT", on_click=on_quit))

# === UI Interface ===
    page.add(
        ft.Text("Input your item"),
        user_input_ui,
        ft.Divider(),
        ft.Text("Current Expenses:"),
        total_text,
        expense_display,
        update_list_ui,
        ft.Divider(),
        exit_app,
    )

    refresh_display()

# === Run App ===
ft.app(target=main)


# === Notes ===
#🎯 目的
#	•	入力フォームで「日付・品目・金額」を登録
#	•	入力データを一覧表示（リスト形式）
#	•	合計金額をリアルタイムで表示
#	•	後半で「CSV保存」なども選択可
#	•	モジュール構造でCLIとGUIを分ける
# CLI Ver.
#1. 日付、品目、金額を1件ずつ入力（辞書で管理）
#2. 入力した支出をリストに追加
#3. 現在のリスト表示＆合計金額を出力
#4. 「続ける or 終了」を選べる
# GUI Ver.
#	•	Fletで以下を実装：
#	•	入力欄（TextField x3）＋追加ボタン
#	•	登録された支出一覧（ListView or Column）
#	•	合計金額を下に表示（Text）
#	•	必要であれば「クリア」「保存」ボタンも追加可能
