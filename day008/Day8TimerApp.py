#Day8 Countdown Timer App

import time
import tkinter as tk

root = tk.Tk()
root.title("Focus Timer")
root.geometry("300x200")
label = tk.Label(root, text="Welcome to the Focus Timer!")
label.pack()

def set_time(seconds):
    global selected_time
    selected_time = seconds
    root.destroy()

btn_10 = tk.Button(root, text="10min", command=lambda: set_time(10 * 60))
btn_25 = tk.Button(root, text="25min", command=lambda: set_time(25 * 60))
btn_50 = tk.Button(root, text="50min", command=lambda: set_time(50 * 60))

btn_10.pack()
btn_25.pack()
btn_50.pack()

entry = tk.Entry(root)
entry.pack()

def start_manual():
    try:
        mins = int(entry.get())
        set_time(mins * 60)
    except ValueError:
        print("Please enter a valid number.")

start_btn = tk.Button(root, text="Start Manual", command=start_manual)
start_btn.pack()

root.mainloop()

#↓CLIで操作していたパターン
#def focus_template():
#    try:
#        user_options = [10, 25, 50]
#        print(f"1. {user_options[0]}mins")
#        print(f"2. {user_options[1]}mins")
#        print(f"3. {user_options[2]}mins")
#        print(f"4. Enter focus time manually.")
#        print(f"5. Add focus time template.") #後で実装
#        print("Enter Q to quit")
#        user_choice = input("Choose focus time from the list above:")
#        if user_choice == "1":
#            print(f"Okay! Let's focus for {user_options[0]}mins!")
#            return int(user_options[0]) * 60
#        elif user_choice == "2":
#            print(f"Okay! Let's focus for {user_options[1]}mins!")
#            return int(user_options[1]) * 60
#        elif user_choice == "3":
#            print(f"Okay! Let's focus for {user_options[2]}mins!")
#            return int(user_options[2]) * 60
#        elif user_choice == "4":
#            focus_time_input = input("Enter the time you want to focus: ")
#            return int(focus_time_input) * 60
#        elif user_choice == "q":
#            exit()
#        else:
#            return
#    except ValueError:
#        print("Invalid input. Enter again.")
#        return focus_template()
#
#def user_input():
#    time_select = int(input("Enter the minutes you want to focus: "))
#    return time_select * 60
# 
#for time_remaining in range(focus_template(), 0, -1):
#    minutes_left, seconds_left = divmod(time_remaining, 60)
#    print(f"{minutes_left:02}:{seconds_left:02}")
#    time.sleep(1)
#print("Timer finished!")



#This is a test to see if I successfuly synced my local env and Github!
#Notes
#✔timerの表示が２→Finished!となるのはUX的に良くない
#✔2-->1-->Finished!となったほうが自然
#✔mm:ssの表示に変換する
#自分で時間を入力するか、テンプレートの時間を選択してタイマーを開始する
#└Windowポップアップを出してマニュアル入力かテンプレ選択でタイマーを開始できるようにする
#timerを途中でやめる機能をつける。特定のキー（ESCかQ）を押すか、GUI版ではキャンセルボタンを押すか

#Learning Notes
#for time_remaining in range(user_input(), 1, -1): --> ..., 0, -1)とした方が、0:00で終了となり自然
#GUIで操作するので、focus_template()などのCLI（コンソールで入力する）は不要
