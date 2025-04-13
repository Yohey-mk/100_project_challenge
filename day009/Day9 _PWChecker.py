#Day9 パスワード強度チェッカー
import string

def check_password(password):
    score = 0
    #最初に長さ、英数字大文字・小文字が含まれているかチェックする
    if len(password) < 8:
        return "Password is too short!"
    if not any(char.isdigit() for char in password):
        return "Password must have at least one digit."
    if not any(char.isalpha() for char in password):
        return "Password must have at least one letter."
    
    else:
        return "Your password is strong."
    



password = input("Enter your password: ")
result = check_password(password)
print(result)





#Learning Notes
#まず最初にやることを定義する。何が必要か？どのような仕組みか？を階層的に明示してみる。
#ユーザーにPWを入力してもらう→判定をくだす
#import string --> 文字列型をimportってどんな役割？


#Ideas
#most common passwordsのリストをcsvなどで作成し、それをインポートして、
#ユーザーが入力したパスワードと一致しているかチェックする。もし一致した場合はAlertを出す
