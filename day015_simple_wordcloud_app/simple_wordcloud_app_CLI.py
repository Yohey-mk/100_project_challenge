# simple_wordcloud_app.py
# CLI Ver.

### === Imports===
import pandas as pd
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt


### === Helper Functions ===
# Load Stopwords
def load_stopwords(csv_file="stopwords.csv"):
    try:
        df = pd.read_csv(csv_file)
        stopwords = df["stopwords"].dropna().tolist() #stopwordsのところにヘッダーをいれる
        return stopwords
    except FileNotFoundError:
        print("No stopwords.csv. Will skip.")
        return []

# CSV Reader
def csv_reader():
    try:
        set_csv_file = input("Enter the csv file name: ")
        df = pd.read_csv(f"{set_csv_file}.csv")
        text_column = df["Content"].dropna().tolist() # ""内に、タイトル名をいれるEx. Title, Content, etc
        return text_column
    except FileNotFoundError:
        return "No such file exist."

# 形態素解析
def text_analyzer(text_column, stopwords=None):
    if stopwords is None:
        stopwords = []

    t = Tokenizer()
    words = []
    for sentence in text_column:
        tokens = t.tokenize(sentence)
        for token in tokens:
            word = token.surface
            part_of_speech = token.part_of_speech.split(',')[0]
            if part_of_speech == '名詞' and word not in stopwords:
                words.append(word)
    return words

# WordCloud Generator
def gen_wordcloud(words):
    text = ' '.join(words)
    wc = WordCloud(font_path="/System/Library/Fonts/ヒラギノ角ゴシック W2.ttc", width=800, height=400, background_color="white").generate(text)

    def show_image():
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        #plt.savefig("wordcloud.png") #一旦画像の保存はコメントアウト
    show_image()


### === App Logics ===
def main():
    data = csv_reader()
    stopwords = load_stopwords("stopwords.csv")
    analyzed_text_data = text_analyzer(data, stopwords)
    gen_wordcloud(analyzed_text_data)

### === Run App ===
if __name__ == '__main__':
    main()


### === Notes ===
# Ideas
#	•	画像ファイルとして保存：wc.to_file("wordcloud.png") 🧙‍♀️✅️やろうかな？
#	•	ストップワード（不要語）の除去：WordCloud(stopwords=...) を活用🧙‍♀️✅️やろうかな？
#	•	形態素解析のカスタマイズ（名詞だけ抽出など）🧙‍♀️✅️やろうかな？
#	•	複数CSV対応：ファイルをループで読み込んで合算 ❎️一旦スキップでいいかも
#	•	GUI版への拡張：Fletを使ってファイル選択や画像表示など 🧙‍♀️✅️GUI版でやる