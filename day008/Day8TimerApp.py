#Day8 Countdown Timer App

import tkinter as tk

root = tk.Tk()
root.title("Focus Timer")
root.geometry("300x400")
label = tk.Label(root, text="Welcome to the Focus Timer!")
label.pack()

running = False
end_flg = False
stop_flg = False

def timer_main(seconds):
    def countdown():
        #nonlocal seconds
        global current_time #外部のcurrent_timeを更新する
        if running and current_time >= 0:
            mins, secs = divmod(current_time, 60)
            time_str = f"{mins:02}:{secs:02}"
            label.config(text=time_str)
            #seconds -= 1
            current_time -= 1
            root.after(1000, countdown)
        elif not running and not end_flg:
            label.config(text="Timer Paused")
        elif end_flg:
            label.config(text="Timer Ended") 
        else:
            label.config(text="Finished!")
    countdown()

#Toggleボタンの導入、タイマー開始/停止時の挙動を制御
def toggle_buttons(state):
    btn_10.config(state=state)
    btn_25.config(state=state)
    btn_50.config(state=state)
    start_manual_btn.config(state=state)
    start_btn.config(state=state)
    #Stop/Endは逆にする
    stop_btn.config(state="normal" if state == "disabled" else "disabled")
    end_btn.config(state="normal" if state == "disabled" else "disabled")


#Startボタンの挙動
def start_button():
    global running
    if running:
        return
    if current_time <= 0:
        label.config(text="Please set a time before starting.")
        return
    running = True
    toggle_buttons("disabled")
    timer_main(current_time) #timer_main()を呼び出すのはタイマーをスタートするとき

start_btn = tk.Button(root, text="Start", command=start_button)
start_btn.pack()

#Stopボタンの挙動→一時停止にする
def stop_button():
    global running, stop_flg
    running = False
    stop_flg = True
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

end_btn = tk.Button(root, text="End", command=end_button)
end_btn.pack()

#秒数の管理状態
current_time = 0
def set_time(seconds, label_minutes): #start_manual_buttonで設定した時間もここで受け取る
    global current_time
    if running:
        return #タイマー実行中ならtimer_main()の呼び出しを無視する
    current_time = seconds
    if label_minutes:
        label.config(text=f"Set: {label_minutes}min\nPress Start")#label_minutesを受け取り、表示


btn_10 = tk.Button(root, text="10min", command=lambda: set_time(10 * 60, 10))#(10 * 60, 10)の, 10-->これがラベル表示に使われる？
btn_25 = tk.Button(root, text="25min", command=lambda: set_time(25 * 60, 25))
btn_50 = tk.Button(root, text="50min", command=lambda: set_time(50 * 60, 50))

btn_10.pack()
btn_25.pack()
btn_50.pack()

entry = tk.Entry(root)
entry.pack()

def start_manual_button():
    try:
        global current_time
        mins = int(entry.get())
        current_time = mins * 60
        set_time(current_time, mins)#(10 * 60, 10)の", 10"と同じ要領で、",mins"を追加→Set a timerを押すと、10minなどを押したときと同じ挙動になった
        label.config(text=f"Set: {mins}min\nPress Start")
        #timer_main(current_time) --> current_timeに時間をセットするだけにして、Startボタンでタイマーを開始するように制御しなおす
    except ValueError:
        print("Please enter a valid number.")

start_manual_btn = tk.Button(root, text="Set a timer", command=start_manual_button)
start_manual_btn.pack()

root.mainloop()

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
#実際にはもうstop_flgは不要。running, current_timeで制御可能
#globalの使い方って？→defの外側で定義された値を持ってくる？（今回だとcurrent_time）
#last to do --> 10min, 25min, 50minを押したとき、set for x min!と表示させる --> set_time()関数を修正する
#How? set_time(x * y, z) --> , zの部分を追加。ここがラベルになるっぽい？
#btn_10 = tk.Button(root, text="10min", command=lambda: set_time(10 * 60, 10))
#label_minutesを追加、label.configで押下された時間をセットし表示する
#def set_time(seconds, label_minutes): 
#    global current_time
#    if running:
#        return #タイマー実行中ならtimer_main()の呼び出しを無視する
#    current_time = seconds
#    if label_minutes:
#        label.config(text=f"Set: {label_minutes}min\nPress Start")#label_minutesを受け取り、表示
