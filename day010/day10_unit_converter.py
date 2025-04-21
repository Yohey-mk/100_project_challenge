#Day10 Unit Converter単位変換アプリ

###imports###
import flet as ft
from datetime import datetime
from zoneinfo import ZoneInfo

###sub-functions###
#km to mile
def km_to_mile(km):
    miles = km * 0.621371
    return miles

#mile to km
def mile_to_km(miles):
    km = miles / 0.621371
    return km

#celcius to fahrenheit
def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

#fahrenheit to celsius
def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    return celsius

#Timezone A to B
def timezone_converter(time, timezone_a, timezone_b):
    timezone_difference = timezone_b - timezone_a
    converted_time = time + timezone_difference
    return converted_time

###main###
def main(page: ft.Page): #ft.pageでは動かなくて、ft.Pageと記述すること！
    value_input = ft.TextField(label="Enter number/time: ", width=300)
    #dropdownを追加して、ドロップダウンに従い上記のvalue_inputを変換するex.num=32, dropdown=f to c --> convert to 0 in c
    dropdown_list = ft.Dropdown(
        convert_menu=[
            ft.dropdown.Option("Timezone"),
            ft.dropdown.Option("km <-> mile"),
            ft.dropdown.Option("Fahrenheigt <-> celsius")],
        options=[
        ft.dropdown.Option("Asia/Tokyo"),
        ft.dropdown.Option("UTC"),],
    value="Asia/Tokyo"
    )
    converted_text = ft.Text("Converted: ")

    #converter function
    def converter(e):
        if convert_menu.value == "Timezone":
            try:
                pass
            except Exception as ex:
                result_text.value = f"Error: {ex}"
###app###
ft.app(target=main)







#ChatGPTからもらった課題とLearning notes
#🎯 Day10：単位変換アプリ（Unit Converter）
#
#題材：
#簡単な単位変換ツールを作ってみよう！例として「距離（km ↔︎ mile）」や「温度（℃ ↔︎ °F）」などを切り替えて変換できるGUIを作成してみよう。
#
#機能要件：
#	•	数値入力欄
#	•	単位の種類を選ぶ（例：距離 or 温度）
#	•	変換方向を選べる（例：km → mile、または逆）
#	•	「変換」ボタンで結果を表示
#	•	見やすいレイアウトと結果表示
#
#Flet UIの構成ヒント：
#	•	数値入力用の TextField
#	•	変換タイプを選択する Dropdown
#	•	変換方向を選択する Radio か Dropdown
#	•	結果を表示する Text や Container
#	•	Button で変換実行
#