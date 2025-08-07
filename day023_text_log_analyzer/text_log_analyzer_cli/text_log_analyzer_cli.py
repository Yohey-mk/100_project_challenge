# text_log_analyzer_cli.py

### === Imports ===
import argparse
from collections import defaultdict, Counter

### === Helper Function ===

### === USERでフィルター
def read_text_log(filter_user=None):
    with open("log_file.txt", "r", encoding="utf-8") as f:
        for line in f:
            try:
                timestamp, username, comment = line.strip().rsplit(":", 2)
                if filter_user is None or username == filter_user:
                    print(f"[{timestamp}] {username}: {comment}")
            except ValueError:
                continue

### === User発言回数ランク
def get_log_lines(filename="log_file.txt"):
    with open("log_file.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
    
def count_user_msg(log_lines):
    counter = Counter()
    for line in log_lines:
        try:
            _, username, _ = line.rsplit(":", 2)
            counter[username] += 1
        except ValueError:
            continue
    return counter

def show_ranking(counter, top_n=None):
    print("\n発言数RANK")
    for i, (user, count) in enumerate(counter.most_common(top_n), 1):
        print(f"{i}: {user} - {count}回")


def main():
    print("\n=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n")
    print("How to use: python module_name.py --x XXXX")
    print("EX: python text_log_analyzer_cli.py --user Alice")
    parser = argparse.ArgumentParser(description="Log Analyzer")
    parser.add_argument("--user", help="指定ユーザの発言だけ表示")
    parser.add_argument("--rank", action="store_true", help="ユーザごとの発言数ランク")
    parser.add_argument("--top", type=int, help="上位N人だけ表示")
    args = parser.parse_args()

    if args.user:
        read_text_log(filter_user=args.user)
    
    if args.rank:
        log_lines = get_log_lines()
        counter = count_user_msg(log_lines)
        show_ranking(counter, top_n=args.top)

    if not args.user and not args.rank:
        parser.print_help() #ここでusageを表示している？

if __name__ == "__main__":
    main()










### === notes ===
#✅ CLI版（第一ステップ）で学べること：
#	•	reモジュールによる 正規表現パターンの設計と抽出
#	•	ログ行を1つずつ処理し、情報を抽出 → 辞書やリストで整理
#	•	CSVへの出力処理（csvモジュールやpandas.to_csv()）
#
#✅ GUI版（Streamlit版）で追加する要素：
#	•	.txtや.logファイルの アップロード（st.file_uploader()）
#	•	パターン選択やカスタム抽出条件の インターフェース（st.selectbox()など）
##	•	CSVダウンロード（st.download_button()）