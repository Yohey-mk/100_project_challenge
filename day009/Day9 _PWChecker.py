#Day9 パスワード強度チェッカー
import string
import csv #csvにあるリストを使いPWの脆弱性をチェックする
import random #password genに使う
import re #連続文字のチェックに使う


#CSVからPWリストを読み込む
def load_pw_list(Most_common_passwords): #get_csv_list()とかを作成して、CSVのアップロード/読み込み機能をつける、または指定フォルダのCheck用PW保管用のCSVファイルを表示する？
    with open("Most_common_passwords.csv", newline='') as csvfile:
        return {row[0] for row in csv.reader(csvfile)}

#連続文字のチェック
def repeated_characters_check(password, repeat_count=3):
    return bool(re.search(rf'(.)\1{{{repeat_count - 1},}}', password)) #bool以降の使い方？？

def check_password(password):
    score = 0
    #passwordがtoo commonかCheck
    common_pw_list = load_pw_list("Most_common_passwords.csv")
    if password in common_pw_list:
        return "Password is too common."
    #最初に長さ、英数字大文字・小文字が含まれているかチェックする
    if len(password) < 8:
        return "Password is too short!"
    if not any(char.isdigit() for char in password):
        return "Password must have at least one digit."
    if not any(char.isalpha() for char in password):
        return "Password must have at least one letter."
    if not any(char.islower() for char in password) or not any(char.isupper() for char in password):
        return "Password must have both lower and upper case letters."
    if not any(char in string.punctuation for char in password):
        return "Password must have at least one special letter."    
    if repeated_characters_check(password):
        return "Password contains repeated characters."
    else:
        return "Your password is strong."
    
#↓def user_options()の条件分岐に組み込んだのでコメントアウト。学びの記録としては残しておく。
#def generate_password(char_length=gen_length):
#    char_length = string.ascii_letters + string.digits + string.punctuation
#    return ''.join(random.choice(char_length) for _ in range(gen_length)) #gen pwにlower/upper caseのどちらも含める
    

def user_options():
    print("""Choose your option:
          1)Generate password
          2)Check your password strength""")
    user_choice = input("Enter your option: ")
    if user_choice == "1":
        gen_length = int(input("Set a length of password generation.\nChoose numbers between 8 - 100: ")) #後に数字/アルファベット（大文字小文字）/記号オンリーなどの組み合わせを選べるようにする
        if gen_length < 8 or gen_length > 100:
            print("Length must be between 8 and 100.")
            return
        else:
            char_length = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
            gen_password = ''.join(random.choice(char_length) for _ in range(gen_length)) #gen pwにlower/upper caseのどちらも含める
            print(f"Generated password: {gen_password}")
    elif user_choice == "2":
        password = input("Enter your password: ")
        result = check_password(password)
        print(result)
    else:
        print("Invalid option. Please choose 1 or 2.")



user_options()

#Learning Notes
#まず最初にやることを定義する。何が必要か？どのような仕組みか？を階層的に明示してみる。
#ユーザーにPWを入力してもらう→判定をくだす
#import string --> 文字列型をimportってどんな役割？
#FileNotFoundError: [Errno 2] No such file or directory: 'Most_common_passwords.csv'
#-->VSCodeで実行しているのが、Day009ではなく、大本の100project_challengeだったのが原因で上記のエラーになっていた
#-->移動したあとにプログラムを実行すると、正常にCSVを読み込み、""Password is too common."も機能した。
#string.ascii_letters --> A - Z, includes upper&lower letters.
#string.ascii_lower/uppercase --> lower or upper letters.
#string.digits --> 0 - 9
#string.punctuation --> Special characters like !@#$%^&*()


#Ideas
#most common passwordsのリストをcsvなどで作成し、それをインポートして、
#ユーザーが入力したパスワードと一致しているかチェックする。もし一致した場合はAlertを出す
#Password generation function
#--> random, stringを使う
#Passwordが連続して同じ英数字を使っていたら駄目とする --> How?

