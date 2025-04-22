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
    #input_fieldは、日時変換とUnit変換では形式が違うから分岐させたほうがいい？Ex. 最初にOptionsを選ばせる→Optionに応じた変換フィールド(input)を作成する？
    input_field = ft.TextField(label="Enter number/time: ", width=300)
    #dropdownを追加して、ドロップダウンに従い上記のvalue_inputを変換するex.num=32, dropdown=f to c --> convert to 0 in c
    #dropdownに渡せるのはlabel, options, value, on_changeなどの公式引数のみ（最初convert_menu=[ft.dropdown.Option...]と書いてエラーになっていた）
    #value="Timezone" -->これは、ドロップダウンのデフォルトの選択肢を決めている。
    convert_menu = ft.Dropdown(
        label="Options: ",
        options=[
            ft.dropdown.Option("Timezone"),
            ft.dropdown.Option("km -> mile"),
            ft.dropdown.Option("Fahrenheit <-> Celsius")],
        value = "Timezone"
    )
    #Timezone変換用のサブオプション
    timezone_from = ft.Dropdown(
        label="From",
        options=[
            ft.dropdown.Option("Asia/Tokyo"),
            ft.dropdown.Option("UTC")],
        value="Asia/Tokyo",
        visible=True
    )

    timezone_to = ft.Dropdown(
        label="To",
        options=[
            ft.dropdown.Option("Asia/Tokyo"),
            ft.dropdown.Option("UTC")],
        value="UTC",
        visible=True
    )
    converted_text = ft.Text("Converted: ")

    #選択肢によってUIを切り替える処理
    def handle_menu_change(e):
        if convert_menu.value == "Timezone":
            timezone_from.visible = True
            timezone_to.visible = True
        elif convert_menu.value == "km -> mile":
            timezone_from.visible = False
            timezone_to.visible = False
        elif convert_menu.value == "Fahrenheit <-> Celsius":
            timezone_from.visible = False
            timezone_to.visible = False
        page.update()

    convert_menu.on_change = handle_menu_change

    #converter function
    def converter(e):
        try:
            if convert_menu.value == "Timezone":
                #選択したプルダウンがTimezoneの場合、入力した文字列をdatetimeに変換
                print("Timezone selected")
                pass
            #最初elif convert_menu == "km -> mile"と書いていて動かなかった。.valueをつけるように注意！
            #convert_menu は Dropdown オブジェクトそのものであり、.value を使って現在の選択値（文字列）を取得しないといけない。
            elif convert_menu.value == "km -> mile":
                num = float(input_field.value)
                km_to_mile(num)
                converted_text.value = f"Converted: {km_to_mile(num)}:.2f miles"
            elif convert_menu.value == "Fahrenheit <-> Celsius":
                pass
        except Exception as ex:
            converted_text.value = f"Error: {ex}"
        page.update()

#Buttons
    convert_button = ft.ElevatedButton("Convert", on_click=converter)

    #UI設定
    page.add(
        convert_menu,
        ft.Row([timezone_from, timezone_to]),
        input_field,
        convert_button,
        converted_text
    )


###app###
ft.app(target=main)





#Learning notes/ideas
#unit変換用の関数が多くて煩雑に見える。。。改善できないかな？
#unit変換用の関数群は別途作成して、その関数群を読み込んで、選択したUnitに対応して関数を呼び出すとか？

#ChatGPTからもらった課題と
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