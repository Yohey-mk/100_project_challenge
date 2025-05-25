#Day 12: 電卓付きカレンダーアプリ（CLI → GUI）

# === imports ===
import flet as ft
from datetime import datetime, timedelta
#moduleのimport
from input_handler import get_user_input, parse_date_input
from calculator import date_calculation
from result_display import print_result

# === Helper / Background functions ===

# === App Logics ===
def main_gui(page: ft.Page):
    page.title = "Calendar with calculator"
    #入力値を保持するための変数（関数内で共有）
    app_state = {"base_date": None, "days_offset": None, "calculation_result": None}

    theme_switch = ft.Switch(label="Light", value=True)
    def toggle_theme_switch(e):
        if theme_switch.value:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        page.update()
    toggle_theme_switch(None)
    theme_switch.on_change = toggle_theme_switch

#日付入力欄の処理
    def handle_submit(e):
        try:
            base_date = parse_date_input(e.control.value)
            app_state["base_date"] = base_date #app_stateにbase_dateの値を保存
            page.controls.append(ft.Text(f"Valid date: {base_date}"))
        except ValueError:
            page.controls.append(ft.Text("Invalid date format. Please use yyyy-mm-dd."))
    date_input_field = get_user_input(handle_submit)
    #page.controls.append(date_input_field)
    page.update()

#日数入力欄の処理
    def handle_days_submit(e):
        try:
            days = int(e.control.value)
            app_state["days_offset"] = days
            offset_days_text.value = f"Offset Days: {days}"
            #page.controls.append(ft.Text(f"Offset Days: {days}"))
        except ValueError:
            page.controls.append(ft.Text("Please enter a valid number."))
        page.update()

#計算ボタン処理
    def handle_calculation(e):
        if app_state["base_date"] is None or app_state["days_offset"] is None:
            page.controls.append(ft.Text("Please input a date first."))
        else:
            result = date_calculation(app_state["base_date"], app_state["days_offset"])
            result_text.value = f"New date: {result.date()} ({result.strftime('%A')})"
            #page.controls.append(ft.Text(f"New date: {result.date()} ({result.strftime('%A')})"))
        page.update()

    def quit_app():
        exit()

# === UI Components ===
    result_text = ft.Text(value="", color="green")
    #user_input_button = ft.ElevatedButton(text="Input", on_click=get_user_input) ###日付入力欄で直接GUIに組み込んでいるので、不要
    days_input_field = ft.TextField(label="Enter how many days before / after:", on_submit=handle_days_submit)
    calc_button = ft.ElevatedButton(text="Calculate", on_click=handle_calculation)
    offset_days_text = ft.Text(value="", color="blue")
    #result_button = ft.ElevatedButton(text="Show Result", on_click=print_result)
    quit_app_button = ft.ElevatedButton(text="Quit", on_click=quit_app)

# === User Interface ===
    page.add(
        theme_switch,
        date_input_field,
        #user_input_button,
        days_input_field,
        calc_button,
        result_text,
        offset_days_text,
        #result_button,
        quit_app_button
    )

# === Run App ===
ft.app(target=main_gui)

#if __name__ == '__main__':
#    main()

#legacy
#def main():
#    base = get_user_input()
#    base_day = base.strftime('%A')
#    new_date = date_calculation(base)
#    new_date_day = new_date.strftime('%A')
#    print_result()
#    print(f"Date: {base} ({base_day})")
#    print(f"New date: {new_date} ({new_date_day})") #debug


#Leaning notes
#🎯目標：
#	•	日付入力から曜日を判定し、さらに簡単な日付計算（○日後や○日前）を行えるCLIアプリを作成。
#	•	GUI版では、日付選択UIと結果表示エリアを備えたアプリに。