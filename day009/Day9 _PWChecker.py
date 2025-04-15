#Day9 パスワード強度チェッカー
import string
import csv #csvにあるリストを使いPWの脆弱性をチェックする
import random #password genに使う

def load_pw_list(Most_common_passwords): #get_csv_list()とかを作成して、CSVのアップロード/読み込み機能をつける、または指定フォルダのCheck用PW保管用のCSVファイルを表示する？
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
    
gen_length = int(input("Set a length of password generation: ")) #後に数字/アルファベット（大文字小文字）/記号オンリーなどの組み合わせを選べるようにする
def generate_password(char_length=gen_length):
    char_length = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(char_length) for _ in range(gen_length)) #gen pwにlower/upper caseのどちらも含める
    
gen_password = generate_password()
print(f"Generated password: {gen_password}")
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
#--> random, stringを使う
#Passwordが連続して同じ英数字を使っていたら駄目とする --> How?

