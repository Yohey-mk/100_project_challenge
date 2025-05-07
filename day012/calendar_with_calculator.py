#Day 12: 電卓付きカレンダーアプリ（CLI → GUI）

# === imports ===
from datetime import datetime, timedelta
#moduleのimport
from input_handler import get_user_input
from calculator import date_calculation
from result_display import print_result

# === Helper / Background functions ===


# === User Interface ===


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