# Day11 Flash Card Study App

###Imports
import random
import csv
import glob #globモジュールで複数ファイルを検索する
from datetime import datetime

###Helper-functions
#スキップ済みの単語を読み込む
def load_skipped_words():
    try:
        with open("skipped_word_list.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return set(row[0] for row in reader if row)
    except FileNotFoundError:
        return set()

skipped_words = load_skipped_words()

csv_files = glob.glob("en-ja_*.csv") #カレントディレクトリにある、"en-ja_"で始まるCSVファイル名をすべて取得
#print("読み込むCSVファイル:", csv_files) #debug用。読み込むCSVを確認。デバッグの際はカレントディレクトリでコードが実行されているかも確認しよう！
cards = {}

for file in csv_files:
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0]: #row -> 行が存在していて（空行ではない）、row[0] -> A列が空ではない
                parts = row[0].split(";") #セミコロンで分割する。「いい;good;;basic, adjective」といった行があった場合、要素１＝いい、要素２＝good、要素３＝””、要素４＝basic, adjectiveと分割している
                if len(parts) >= 2: #row and row[0]でチェックした行の要素が2以上なら次へ進む
                    eng, jp = parts[1].strip(), parts[0].strip() #engにB列、jpにA列の要素を割り当てる。.strip()で余計なスペースや改行を取り除く
                    #cards[eng] = jp #ここでスキップ単語を入れる前に単語を追加していた！そのため、スキップ単語が表示されてしまう挙動をとっていた。
                    if eng not in skipped_words: #ここでスキップ単語を弾く
                        cards[eng] = jp

#スコア記録用の関数
def save_score_log(correct_count, skipped_count, total_words, correct_rate):
    today = datetime.now().strftime("%Y-%m-%d")
    with open("score_log.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([today, correct_count, skipped_count, total_words, f"{correct_rate:.1f}%"])

#スキップした単語の保存用関数
def skipped_words_log(skipped_words):
    with open("skipped_word_list.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for word in skipped_words:
            writer.writerow([word])

###UI Components

###App Logic

###Run App

#Notes / ToDo

###Legacy

#CLI版
#cards = {
#    "apple": "リンゴ",
#    "banana": "バナナ",
#    "grape": "ぶどう",
#    "orange": "オレンジ",
#    "peach": "モモ"
#}

def show_card():
    print("*Press q to quit") #GUI版ではキャンセルボタンを設置で途中でやめられるようにする
    #shuffleした辞書
    items = list(cards.items())
    random.shuffle(items)
    #setting up for starting the game
    word_count_all = len(items)
    user_score = 0
    skipped_word_count = 0
    game_stage = 0
    skipped_word_list = []

    for eng, jp in items:
        user_input = input(f"{eng}の意味は？: ").lower()
        game_stage += 1
        if user_input == "q":
            break
        elif user_input == "s":
            skipped_word_count += 1
            skipped_word_list.append(eng)
            print("skipped\n")
        else:
            if user_input.strip() == jp:
                user_score += 1
                print("Correct!\n")
            else:
                print(f"答え: {jp}\n")
    print("Finished!")
    total_score = user_score / (game_stage - skipped_word_count) * 100
    print(f"Your score: {total_score:.1f}%") #正答数/(総出題数-Skipped数)、改行して→総出題数X、正解数Y、Skipped数Z、残り問題数xx、、、みたいな表示のほうがユーザフレンドリーかも？
    print(f"""Total game stage: {game_stage}
Correct answers: {user_score}
Skipped answers: {skipped_word_count}
Remaining word list: {word_count_all - (user_score + skipped_word_count)}
Skipped word(s) list: {', '.join(skipped_word_list)}""")
    try_again = input("Would you like to try again? y/n: ").lower()
    if try_again == "y":
        show_card()
    else:
        print("Great job! Have a nice day!")
        save_score_log(user_score, skipped_word_count, game_stage, total_score)
        skipped_words_log(skipped_word_list)


if __name__ == "__main__":
    show_card()


#課題
#🎯 題材
#フラッシュカード（単語帳）形式で学習できる簡単なアプリを作成してみましょう。英単語→日本語のような形式で、1つずつカードを表示し、「答えを見る」「次へ進む」などの機能を備えたものです。
#💡 目的
#	•	リストや辞書の操作に慣れる
#	•	イベント処理や画面更新の練習（GUI版ならFletやTkinter、CLI版でもOK）
#	•	「状態の保持（現在のカード番号）」や「シャッフル」「繰り返し表示」などの工夫が可能