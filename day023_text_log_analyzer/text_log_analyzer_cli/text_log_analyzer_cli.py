# text_log_analyzer_cli.py

### === Imports ===
import pandas as pd
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

### === Helper Function ===
def read_text_log():
    with open("log_file.txt", "r", encoding="utf-8") as f:
        for line in f:
            timestamp, username, comment = line.strip().rsplit(":", 2)
            print(f"[{timestamp}] {username}: {comment}")

def main():
    read_text_log()

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