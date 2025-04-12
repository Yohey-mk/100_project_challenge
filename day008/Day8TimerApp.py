#Day8 Countdown Timer App

import tkinter as tk

root = tk.Tk()
root.title("Focus Timer")
root.geometry("300x400")
label = tk.Label(root, text="Welcome to the Focus Timer!")
label.pack()

running = False
end_flg = False

def timer_main(seconds):
    def countdown():
        nonlocal seconds
        if running and seconds >= 0:
            mins, secs = divmod(seconds, 60)
            time_str = f"{mins:02}:{secs:02}"
            label.config(text=time_str)
            seconds -= 1
            root.after(1000, countdown)
        elif not running and not end_flg:
            label.config(text="Timer Paused")
        elif not running and end_flg:
            label.config(text="Timer Ended.") 
        else:
            label.config(text="Finished!")
    countdown()

#Toggleボタンの導入、タイマー開始/停止時の挙動を制御
def toggle_buttons(state):
    if not running and not end_flg:
        btn_10.config(state="normal")
        btn_25.config(state="normal")
        btn_50.config(state="normal")
        start_btn.config(state="normal")
        stop_btn.config(state="disabled")
        end_btn.config(state="disabled")
        start_manual_btn.config(state="normal")
    elif running and not end_flg:
        btn_10.config(state="disabled")
        btn_25.config(state="disabled")
        btn_50.config(state="disabled")
        start_btn.config(state="disabled")
        stop_btn.config(state="normal")
        end_btn.config(state="normal")
        start_manual_btn.config(state="disabled")
    elif not running and end_flg:
        btn_10.config(state="normal")
        btn_25.config(state="normal")
        btn_50.config(state="normal")
        start_btn.config(state="normal")
        stop_btn.config(state="disabled")
        end_btn.config(state="disabled")
        start_manual_btn.config(state="normal")
    else:
        return
#Startボタンの挙動
def start_button():
    global running
    running = True
    toggle_buttons("disabled")
    timer_main(current_time)

start_btn = tk.Button(root, text="Start", command=start_button)
start_btn.pack()

#Stopボタンの挙動→一時停止にする
def stop_button():
    global running
    global end_flg
    running = False
    end_flg = False
    toggle_buttons("normal")
    label.config(text="Timer Paused")
    
stop_btn = tk.Button(root, text="Pause", command=stop_button)
stop_btn.pack()

#Endボタンでタイマーが途中でも終了する
def end_button():
    global running, end_flg #globalのあとに、,で続けてフラグをつけることができる
    running = False
    end_flg = True
    toggle_buttons("normal")
    label.config(text="Timer Ended")

end_btn = tk.Button(root, text="End", command=end_button)
end_btn.pack()

#秒数の管理状態
current_time = 0
def set_time(seconds):
    global current_time
    if running:
        return #タイマー実行中ならtimer_main()の呼び出しを無視する
    current_time = seconds
    timer_main(current_time)


btn_10 = tk.Button(root, text="10min", command=lambda: set_time(10 * 60))
btn_25 = tk.Button(root, text="25min", command=lambda: set_time(25 * 60))
btn_50 = tk.Button(root, text="50min", command=lambda: set_time(50 * 60))

btn_10.pack()
btn_25.pack()
btn_50.pack()

entry = tk.Entry(root)
entry.pack()

def start_manual_button():
    try:
        global running, end_flg
        running = True
        end_flg = False
        mins = int(entry.get())
        set_time(mins * 60)
        toggle_buttons("disabled")
    except ValueError:
        print("Please enter a valid number.")

start_manual_btn = tk.Button(root, text="Start Manual", command=start_manual_button)
start_manual_btn.pack()

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
#✔自分で時間を入力するか、テンプレートの時間を選択してタイマーを開始する
#✔└Windowポップアップを出してマニュアル入力かテンプレ選択でタイマーを開始できるようにする
#timerを途中でやめる機能をつける。特定のキー（ESCかQ）を押すか、GUI版ではキャンセルボタンを押すか

#Learning Notes
#✔for time_remaining in range(user_input(), 1, -1): --> ..., 0, -1)とした方が、0:00で終了となり自然
#✔GUIで操作するので、focus_template()などのCLI（コンソールで入力する）は不要
#"Please enter a valid number" --> Popupまたはウインドウ上で表示したほうがわかりやすい
#現状はCLI上でPlease...と表示される
#tkinter.messageboxというのがあるっぽいので、それを使えばPopupでエラーメッセージを出せそう？
#nonlocalって何？(local環境に依存しないってことかな？)
#root, label, .pack, tk.Button, command=lambda, .mainloopの使い方って？
#runningフラグを使ってタイマーを管理 → 例if running and seconds >= 0:
#つまり、running flgがTrue/FalseでStart/Stopを制御する(True = 1, False = 0なので)
#課題：いくつもボタンを押すと、同時に複数のタイマーが開始されるので、もしすでにタイマーが動いている場合は、
#他の時間のボタンやマニュアル入力をしても機能しないようにする

