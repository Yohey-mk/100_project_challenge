# Day11 Flash Card Study App

###Imports
import flet as ft
import random
import csv
import glob #globモジュールで複数ファイルを検索する
from datetime import datetime
import asyncio
import os

###Helper-functions(background functions)
#スキップ済みの単語を読み込む
def load_skipped_words():
    try:
        with open("skipped_word_list.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return {row[0]: row[1] for row in reader if row and len(row) >= 2}
    except FileNotFoundError:
        return {}

#print("読み込むCSVファイル:", csv_files) #debug用。読み込むCSVを確認。デバッグの際はカレントディレクトリでコードが実行されているかも確認しよう！

#cardsとskipped_cardsを関数にまとめる
def load_cards():
    cards = {}
    skipped_cards = {}
    skipped_words = load_skipped_words()
    csv_files = glob.glob("en-ja_*.csv") #カレントディレクトリにある、"en-ja_"で始まるCSVファイル名をすべて取得

    #通常cardsの整理
    for file in csv_files:
        with open(file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0]: #row -> 行が存在していて（空行ではない）、row[0] -> A列が空ではない
                    parts = row[0].split(";") #セミコロンで分割する。「いい;good;;basic, adjective」といった行があった場合、要素１＝いい、要素２＝good、要素３＝””、要素４＝basic, adjectiveと分割している
                    if len(parts) >= 2: #row and row[0]でチェックした行の要素が2以上なら次へ進む
                        eng, jp = parts[1].strip(), parts[0].strip() #engにB列、jpにA列の要素を割り当てる。.strip()で余計なスペースや改行を取り除く
                        if eng not in skipped_words: #ここでスキップ単語を弾く
                            cards[eng] = jp

    #skipped cardsの整理
    skipped_cards = dict(skipped_words)
    return cards, skipped_cards

#スコア記録用の関数
def save_score_log(correct_count, skipped_count, total_words, correct_rate):
    today = datetime.now().strftime("%Y-%m-%d")
    with open("score_log.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([today, correct_count, skipped_count, total_words, f"{correct_rate:.1f}%"])

#スキップした単語の保存用関数
def skipped_words_log(skipped_word_list):
    with open("skipped_word_list.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for eng, jp in skipped_word_list:
            writer.writerow([eng, jp])

#スキップした単語をスキップリストからリムーブする
def remove_skipped_word(eng, jp):
    try:
        with open("skipped_word_list.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = [row for row in reader if row and len(row) >= 2]

        filtered_rows = [row for row in rows if not (row[0] == eng and row[1] == jp)]

        with open("skipped_word_list.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(filtered_rows)

        print(f"Removed {eng} ({jp}) from skipped word list.")

    except FileNotFoundError:
        print("No skipped_word_list.csv file found.")

###App Logic
#スコアの計算式関数
def score_calculation(user_score, game_stage, skipped_word_count):
    #setting up for starting the game
    result_score = (user_score / (game_stage - skipped_word_count))
    return result_score

#通常ゲームの関数。復習モードをここから選べるようにする。復習モードの関数は別で作成する。
#ループや分岐で中身が長くなっているから、役割ごとに分割して関数化したほうがいいかも？
def show_card_normal(page: ft.Page, cards: dict):
    eng, jp = random.choice(list(cards.items()))
    skipped_word_list = []

    async def answer_submit(e):
        answer = input_field.value.strip()
        if answer == jp:
            result_text.value = "Correct!"
        elif answer == "s":
            skipped_word_list.append((eng, jp))
        else:
            result_text.value = f"Wrong answer. Correct answer: {jp}"
        page.update()
        await asyncio.sleep(1)
        show_card_normal(page, cards)

    input_field = ft.TextField(hint_text="Enter your answer", on_submit=answer_submit)
    result_text = ft.Text("")
    back_button = ft.ElevatedButton(text="Home", on_click=lambda e: show_home(page))

    page.controls.clear()
    page.add(
        ft.Text(f"What does '{eng} mean?"),
        input_field,
        result_text,
        back_button
    )
    page.update()

#復習モードの関数
def review_mode(page: ft.Page, skipped_cards: dict):
    eng, jp = random.choice(list(skipped_cards.items()))

    async def answer_submit(e):
        answer = input_field.value.strip()
        if answer == "r":
            result_text.value = "Move onto the next word"
            page.update()
        else:
            result_text.value = f"Answer: {jp}"
        page.update()
        await asyncio.sleep(1)
        review_mode(page, skipped_cards)

    input_field = ft.TextField(hint_text="Enter R if remembered", on_submit=answer_submit)
    result_text = ft.Text("")
    back_button = ft.ElevatedButton(text="Home", on_click=lambda e: show_home(page))

    page.controls.clear()
    page.add(
        ft.Text(f"What does '{eng} mean?"),
        input_field,
        result_text,
        back_button,
    )
    page.update()

def quit_app(e):
    os._exit(0)

def show_home(page: ft.Page):
    page.controls.clear() #一度ページをまっさらにして、以下にボタンなどを再配置する
    cards, skipped_cards = load_cards()
    home_button_normal = ft.ElevatedButton(text="Study new words", on_click=lambda e: show_card_normal(page, cards))
    home_button_review = ft.ElevatedButton(text="Review mode", on_click=lambda e: review_mode(page, skipped_cards))
    game_quit_button = ft.ElevatedButton(text="Quit", on_click=quit_app)
    page.add(
        home_button_normal,
        home_button_review,
        game_quit_button
    )
    page.update()

#Play game *play modeに応じてshow_cardと復習モードを切り替える -> ###mainで呼び出すのはこちらにする。
def play_mode():
    cards, skipped_cards = load_cards()
    while True:
        game_mode = input("Which mode to play? Select 1 - 3.\n1. Study new words\n2. Review words\n3. Quit game\nYour option: ")
        if game_mode == "1":
            show_card_normal(cards)
        elif game_mode == "2":
            review_mode(skipped_cards)
        elif game_mode == "3":
            print("Bye!")
            break
        else:
            print("Choose your option from 1 - 3.")

###Main (GUI ver)
def main(page: ft.Page):
    page.title = "Flash Study"
    theme_switch = ft.Switch(label="Dark", value=False)
    def toggle_theme(e): #eはイベントを受け取る、fletだと基本こんな感じで書く
        if theme_switch.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()
    toggle_theme(None) #デフォルトはライトモード
    theme_switch.on_change = toggle_theme
    #Game Start
    def start_game_normal(e):
        #show_card()などをここで呼び出し、以下のボタンで選択肢に応じてゲーム開始
        cards, _ = load_cards()
        show_card_normal(page, cards)
    
    def start_game_review(e):
        skipped_cards, _ = load_cards()
        review_mode(page, skipped_cards)

    def game_cancel():
        exit()

###UI Components_Buttons
    game_start_normal_mode = ft.ElevatedButton(text="Study new words", on_click=start_game_normal)
    game_start_review_mode = ft.ElevatedButton(text="Review mode", on_click=start_game_review)
    game_cancel_button = ft.ElevatedButton(text="Cancel", on_click=game_cancel)

###UI Components
    page.add(
        theme_switch,
        game_start_normal_mode,
        game_start_review_mode,
        game_cancel_button
    )

###Run App
ft.app(target=main)

###Legacy
#def show_card(cards):
#    print("*Press q to quit") #GUI版ではキャンセルボタンを設置し、途中でやめられるようにする
#    skipped_word_list = []
#
#    for eng, jp in items:
#        user_input = input(f"{eng}の意味は？: ").lower()
#        game_stage += 1
#        if user_input == "q":
#            break
#        elif user_input == "s":
#            skipped_word_count += 1
#            skipped_word_list.append((eng, jp))
#            print("skipped\n")
#        else:
#            if user_input.strip() == jp:
#                user_score += 1
#                print("Correct!\n")
#            else:
#                print(f"答え: {jp}\n")
#
#    print("Finished!")
#    total_score = user_score / (game_stage - skipped_word_count) * 100
#    print(f"Your score: {total_score:.1f}%") #正答数/(総出題数-Skipped数)、改行して→総出題数X、正解数Y、Skipped数Z、残り問題数xx、、、みたいな表示のほうがユーザフレンドリーかも？
#    skipped_str_list = [f"{eng}({jp})" for eng, jp in skipped_word_list] #ここにタプルのリストを表示用の文字列に変換する
#    print(f"""Total game stage: {game_stage}
#Correct answers: {user_score}
#Skipped answers: {skipped_word_count}
#Remaining word list: {word_count_all - (user_score + skipped_word_count)}
#Skipped word(s) list: {', '.join(skipped_str_list)}""")
#    try_again = input("Would you like to try again? y/n: ").lower()
#    if try_again == "y":
#        show_card(cards)
#    else:
#        print("Great job! Have a nice day!")
#        save_score_log(user_score, skipped_word_count, game_stage, total_score)
#        skipped_words_log(skipped_word_list)

###main(CLI ver)
#if __name__ == "__main__":
#    play_mode()


#課題
#🎯 題材
#フラッシュカード（単語帳）形式で学習できる簡単なアプリを作成してみましょう。英単語→日本語のような形式で、1つずつカードを表示し、「答えを見る」「次へ進む」などの機能を備えたものです。
#💡 目的
#	•	リストや辞書の操作に慣れる
#	•	イベント処理や画面更新の練習（GUI版ならFletやTkinter、CLI版でもOK）
#	•	「状態の保持（現在のカード番号）」や「シャッフル」「繰り返し表示」などの工夫が可能

#Notes / ToDo

#4.27
#スコア記録用の関数とスキップした単語を保存する関数の作成

#4.28~
#	1.	復習モードの搭載
#	•	スキップした単語だけを出題するモード
#	•	普通のモードと切り替え可能にする
#	2.	スキップリストから単語を削除できる機能
#	•	「もう覚えた！」って単語はスキップリストから消して、通常出題に戻す