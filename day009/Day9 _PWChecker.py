#Day9 パスワード強度チェッカー
import string
import csv #csvにあるリストを使いPWの脆弱性をチェックする

def load_pw_list(Most_common_passwords): #get_csv()とかを作成して、CSVのアップロード/読み込み機能をつける、または指定フォルダのCheck用PW保管用のCSVファイルを表示する
    with open("Most_common_passwords.csv", newline='') as csvfile:
        return {row[0] for row in csv.reader(csvfile)}

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
    else:
        return "Your password is strong."
    

password = input("Enter your password: ")
result = check_password(password)
print(result)





#Learning Notes
#まず最初にやることを定義する。何が必要か？どのような仕組みか？を階層的に明示してみる。
#ユーザーにPWを入力してもらう→判定をくだす
#import string --> 文字列型をimportってどんな役割？
#FileNotFoundError: [Errno 2] No such file or directory: 'Most_common_passwords.csv'
#-->VSCodeで実行しているのが、Day009ではなく、大本の100project_challengeだったのが原因で上記のエラーになっていた
#-->移動したあとにプログラムを実行すると、正常にCSVを読み込み、""Password is too common."も機能した。


#Ideas
#most common passwordsのリストをcsvなどで作成し、それをインポートして、
#ユーザーが入力したパスワードと一致しているかチェックする。もし一致した場合はAlertを出す
#Password generation function
#Passwordが連続して同じ英数字を使っていたら駄目とする --> How?

