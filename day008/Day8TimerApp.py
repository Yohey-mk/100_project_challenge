import time

def user_input():
    time_select = int(input("Enter the minutes you want to focus: "))
    return time_select * 60

for time_remaining in range(user_input(), 1, -1):
    minutes_left, seconds_left = divmod(time_remaining, 60)
    print(f"{minutes_left:02}:{seconds_left:02}")
    time.sleep(1)
print("Timer finished!")



#This is a test to see if I successfuly synced my local env and Github!
#Notes
#timerの表示が２→Finished!となるのはUX的に良くない
#2-->1-->Finished!となったほうが自然
#mm:ssの表示に変換する
#自分で時間を入力するか、テンプレートの時間を選択してタイマーを開始する
#└Windowポップアップを出してマニュアル入力かテンプレ選択でタイマーを開始できるようにする
#timerを途中でやめる機能をつける。特定のキー（ESCかQ）を押すか、GUI版ではキャンセルボタンを押すか