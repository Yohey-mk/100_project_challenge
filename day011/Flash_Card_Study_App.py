# Day11 Flash Card Study App
import random

#CLI版
cards = {
    "apple": "リンゴ",
    "banana": "バナナ",
    "grape": "ぶどう",
    "orange": "オレンジ",
    "peach": "モモ"
}

def show_card():
    print("*Press q to quit")
    #shuffleした辞書
    items = list(cards.items())
    random.shuffle(items)
    for eng, jp in items:
        user_input = input(f"{eng}の意味は？").lower()
        if user_input == "q":
            break
        else:
            print(f"答え: {jp}\n")
    print("Finished! Would you like to try again? y/n")
    try_again = input("y/n: ").lower()
    if try_again == "y":
        show_card()
    else:
        print("Gret job! Have a nice day!")


if __name__ == "__main__":
    show_card()


#課題
#🎯 題材
#フラッシュカード（単語帳）形式で学習できる簡単なアプリを作成してみましょう。英単語→日本語のような形式で、1つずつカードを表示し、「答えを見る」「次へ進む」などの機能を備えたものです。
#💡 目的
#	•	リストや辞書の操作に慣れる
#	•	イベント処理や画面更新の練習（GUI版ならFletやTkinter、CLI版でもOK）
#	•	「状態の保持（現在のカード番号）」や「シャッフル」「繰り返し表示」などの工夫が可能