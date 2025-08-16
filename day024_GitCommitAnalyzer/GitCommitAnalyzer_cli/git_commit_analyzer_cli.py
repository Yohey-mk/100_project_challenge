# git_commit_analyzer_cli.py

### === Import ===
import subprocess
from datetime import datetime
from collections import Counter
import pandas as pd
from pandas.api.types import CategoricalDtype

### === Functions ===
def get_git_log(command=None):
    if command is None:
        command = ["git", "log", "--pretty=format:'%h|%an|%ad|%s'", "--date=iso"]
    try:
        result = subprocess.run(
            command, #"--oneline", "log -> status"などで取得内容を変更する
            capture_output=True,
            text=True,
            check=True
        )
        commits = []
        for line in result.stdout.split("\n"):
            try:
                commit_hash, author, date_str, message = line.split("|", 3)
                date_obj = datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S %z")
                commits.append({
                    "hash": commit_hash,
                    "author": author,
                    "date": date_obj,
                    "message": message
                })
            except ValueError:
                continue
        return commits
    except subprocess.CalledProcessError as e:
        print("Error: ", e.stderr or str(e))
        return []

### 分析処理
# コミッター別
def filter_by_committer(df):
    filtered_by_committer = df.groupby(df['author']).size().sort_values(ascending=False)
    return filtered_by_committer

# ランキング用
def filter_by_user(df):
    counter = Counter()
    for _, row in df.iterrows():
        counter[row['author']] += 1
    return counter

def show_ranking(counter, top_n=None):
    lines = []
    for i, (username, count) in enumerate(counter.most_common(top_n), 1):
        lines.append(f"{i}: {username} - {count}")
        return "\n".join(lines)

# 曜日別集計
def filter_by_weekdays(df):
    df_copy = df.copy()
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    cat_type = CategoricalDtype(categories=weekday_order, ordered=True)
    df_copy['weekday'] = df_copy['date'].dt.day_name().astype(cat_type)
    filtered_by_date = df_copy.groupby('weekday').size().sort_index()
    return filtered_by_date

# 時間帯別集計
def filter_by_time(df):
    filtered_by_time = df.groupby(df['date'].dt.hour).size().sort_index()
    return filtered_by_time

# Outputs
log_output = get_git_log()
df = pd.DataFrame(log_output)
print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nLatest Summary")
print(df.head(10))
# 分析オプション
while True:
    print('Choose your option:\n1.Filter by committer\n2.Filter by weekdays\n3.Filter by hour\n4.Show rankings\n5.Quit app')
    try:
        user_input = int(input('Your choice: '))
    except ValueError:
        print('Invalid input.')
    # コミッター別集計
    if user_input == 1:
        print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nCount by commiter")
        print(filter_by_committer(df))
    # 曜日別Output
    elif user_input == 2:
        print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nCount by date name")
        print(filter_by_weekdays(df))
    # 時間帯別Output
    elif user_input == 3:
        print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nCount by hour")
        print(filter_by_time(df))
    # コミッターランキング
    elif user_input == 4:
        filtered_count = filter_by_user(df)
        print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nRanking")
        print(show_ranking(filtered_count, top_n=10))
    # Quit App
    elif user_input == 5:
        exit()
    else:
        print("Invalid input.")




# Notes
#
#	1.	モジュールの準備
#	•	subprocess（Gitコマンド実行用）
#	•	argparse（CLIオプション管理）
#	•	collections.Counter（集計）
#	•	datetime（日付・時間処理）
#⸻
#	2.	Gitログ取得関数
#def get_git_log():
#    # git log --pretty=format:"%H|%an|%ad|%s" --date=iso
#    # 戻り値はリスト形式
#💡 Git コマンドとの組み合わせ例
#	•	git log --oneline → コミット履歴取得
#	•	git status → 変更状況取得
#	•	git diff → 差分取得
#	•	git branch → ブランチ一覧取得
#⸻
#	3.	データパース関数
#	•	コミットハッシュ
#	•	コミッター名
#	•	日時（datetime型に変換）
#	•	メッセージ
#⸻
#	4.	分析処理
#	•	コミッター別集計
#	•	曜日別集計
#	•	時間帯別集計
#	•	メッセージ単語頻度（オプション）
#⸻
#	5.	表示機能
#	•	コマンドライン出力を見やすく（ランキング形式など）
#	•	--top N で上位N件だけ表示できるように
#	•	--since YYYY-MM-DD / --until YYYY-MM-DD で期間絞り込み
#⸻
#	6.	argparseでモード切替
#	•	--by-user → ユーザー別集計
#	•	--by-day → 曜日別集計
#	•	--by-hour → 時間帯別集計
#	•	--word-count → メッセージ単語集計
#⸻
#	7.	メイン関数
#	•	引数を解析
##	•	選択されたモードで分析
#	•	結果出力