#Day9 パスワード強度チェッカー
import string
import csv #csvにあるリストを使いPWの脆弱性をチェックする
import random #password genに使う
import re #連続文字のチェックに使う



#CSVからPWリストを読み込む
def load_pw_list(csv_filename="Most_common_passwords"): #get_csv_list()とかを作成して、CSVのアップロード/読み込み機能をつける、または指定フォルダのCheck用PW保管用のCSVファイルを表示する？
    with open(csv_filename, newline='') as csvfile:
        return {row[0] for row in csv.reader(csvfile)} #❓️row[0] for row in...-->1列目の数だけ1列目を返す、という読み方で合っている？

#連続文字のチェック(同じ文字が repeat_count 回以上連続しているかチェック（例: aaa, 1111）)
def repeated_characters_check(password, repeat_count=3):
    return bool(re.search(rf'(.)\1{{{repeat_count - 1},}}', password)) #bool以降の使い方？？

def check_password(password):
    score = 0 #scoreベースにしないなら不要
    message = [] #message.append("エラーの理由")といった感じで何故判定がアウトになるかをユーザーに提示する
    #passwordがtoo commonかCheck
    common_pw_list = load_pw_list("Most_common_passwords.csv")
    if password in common_pw_list:
        message.append("Too common")
    #最初に長さ、英数字大文字・小文字が含まれているかチェックする
    if len(password) < 8:
        message.append("Too short")
    if not any(char.isdigit() for char in password):
        message.append("Missing digit")
    if not any(char.isalpha() for char in password):
        message.append("Missing letter")
    if not any(char.islower() for char in password) or not any(char.isupper() for char in password):
        message.append("Needs both lower and upper case letters")
    if not any(char in string.punctuation for char in password):
        message.append("Missing special letter")  
    if repeated_characters_check(password):
        message.append("Contains repeated characters")
    if not message:
        return "Your password is strong"
    else:
        return "Weak password. Needs to improve: " + ', '.join(message)
    
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
            #❓️↓のランダム生成だと、意図した挙動（大文字・小文字と数字記号をすべて組み合わせる）にならないので、改善が必要
            #char_length = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
            #gen_password = ''.join(random.choice(char_length) for _ in range(gen_length)) #gen pwにlower/upper caseのどちらも含める
            #✅️Newランダムパスワード生成↓ char_poolに使われる文字列（lowercase, uppercase, digits, punctuation）を格納する
            char_pool = [
                random.choice(string.ascii_lowercase),
                random.choice(string.ascii_uppercase),
                random.choice(string.digits),
                random.choice(string.punctuation)
            ]
            #rest_charactersはletters,digits,punctuationで構成、char_poolは設定したPWの文字数マイナス4をした残りの数だけ、rest_charactersから英数字記号を持ってくる
            if gen_length:
                rest_characters = string.ascii_letters + string.digits + string.punctuation
                #char_pool +=[]で、もともと生成したchar_pool(4文字)に加えて、英数字記号を加える
                char_pool += [random.choice(rest_characters) for _ in range(gen_length - 4)]
            #random.choice(x)は、xの中からランダムに選択する、random.shuffle(y)は、yをランダムに入れ替える
            random.shuffle(char_pool)#ここで最初に生成した4文字+(gen_length-4)の生成した文字列を入れ替える
            gen_password = ''.join(char_pool)
            print(f"Generated password: {gen_password}")
    elif user_choice == "2":
        password = input("Enter your password: ")
        if not password.strip(): #空白を入力された場合の対処
            print("Password cannot be empty.")
            return
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
#''.join(char_pool) は、リストを文字列に変換するお決まりの方法。
#→ リスト ['A', 'b', '1', '%'] → 'Ab1%' にまとめる。
#今回のケースだと、['1','(','6','d','k',':','`','c','J','D','/','J','6','\']みたいになっているリストを、
#1(6dk:`cJD/J6\と結合する役割を果たす。
#random.choice() は1文字だけ選ぶが、
#random.choices()（複数形）は複数選ぶ（重複あり）という違いも覚えておくと便利！


#Ideas
#most common passwordsのリストをcsvなどで作成し、それをインポートして、
#ユーザーが入力したパスワードと一致しているかチェックする。もし一致した場合はAlertを出す
#Password generation function
#--> random, stringを使う
#Passwordが連続して同じ英数字を使っていたら駄目とする --> How?

#ChatGPTからの提案
#🌟おまけ：GUI版にしたら面白くなるポイント
#	•	判定メッセージをラベルで表示
#	•	「生成ボタン」で自動生成 → そのままコピペ可能
#	•	入力ボックスでリアルタイムに強度チェック（発展編）
#	1.	強度スコアを導入（例：5点満点で）
#	2.	GUI化（Tkinter）
#	3.	「辞書に登録された単語を含んでいたらNG」などの応用ルール
#	4.	複数のチェック項目の可視化（何が足りないかを明示）