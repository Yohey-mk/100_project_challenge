#Day 12: 電卓付きカレンダーアプリ（CLI → GUI）

###imports
from datetime import datetime, timedelta

# === Helper / Background functions ===


# === User Interface ===
def get_user_input():
    date_input = input("enter a date(yyyy-mm-dd): ")
    base_date = datetime.strptime(date_input, "%Y-%m-%d")
    return base_date

def date_calculation(base_date):
    input_new_date = int(input("Enter how many days before / after you want to know: "))
    new_date_result = base_date + timedelta(input_new_date)
    return new_date_result

def print_result(): #GUI化のときに使う
    pass

# === UI Components ===

# === App Logics ===
def main():
    base = get_user_input()
    base_day = base.strftime('%A')
    new_date = date_calculation(base)
    new_date_day = new_date.strftime('%A')
    print_result()
    print(f"Date: {base} ({base_day})")
    print(f"New date: {new_date} ({new_date_day})") #debug

# === Run App ===
if __name__ == '__main__':
    main()




#Leaning notes
#🎯目標：
#	•	日付入力から曜日を判定し、さらに簡単な日付計算（○日後や○日前）を行えるCLIアプリを作成。
#	•	GUI版では、日付選択UIと結果表示エリアを備えたアプリに。