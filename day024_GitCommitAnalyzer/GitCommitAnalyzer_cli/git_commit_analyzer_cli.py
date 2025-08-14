# git_commit_analyzer_cli.py

### === Import ===
import subprocess
from datetime import datetime
from collections import Counter
import pandas as pd
from pandas.api.types import CategoricalDtype

### === Functions ===
def get_git_log(command=["git", "log", "--pretty=format:'%h|%an|%ad|%s'", "--date=iso"]):
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
    print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nCount by commiter")
    filtered_by_committer = df.groupby(df['author']).size().sort_values(ascending=False)
    print(filtered_by_committer)

# ランキング用
def filter_by_user(df):
    counter = Counter()
    for _, row in df.iterrows():
        counter[row['author']] += 1
    return counter

def show_ranking(counter, top_n=None):
    print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nRanking")
    for i, (username, count) in enumerate(counter.most_common(top_n), 1):
        print(f"{i}: {username} - {count}")

# 曜日別集計
def filter_by_weekdays(df):
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    cat_type = CategoricalDtype(categories=weekday_order, ordered=True)
    df['weekday'] = df['date'].dt.day_name().astype(cat_type)
    print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nCount by date name")
    #filtered_by_date = df.groupby(df['date'].dt.day_name()).size().sort_values(ascending=False)
    filtered_by_date = df.groupby('weekday').size().sort_index()
    print(filtered_by_date)

# 時間帯別集計
def filter_by_time(df):
    print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nCount by hour")
    filtered_by_time = df.groupby(df['date'].dt.hour).size().sort_index()
    print(filtered_by_time)


# Outputs
log_output = get_git_log()
df = pd.DataFrame(log_output)
print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nLatest Summary")
print(df.head(10))
# コミッター別集計
filter_by_committer(df)
#print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\nCount By User")
#count_by_user = df.groupby("author").size().sort_values(ascending=False)
#print(count_by_user.head(10))
# 曜日別Output
filter_by_weekdays(df)
# 時間帯別Output
filter_by_time(df)
# コミッターランキング
filtered_count = filter_by_user(df)
show_ranking(filtered_count, top_n=10)
print("-------")




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