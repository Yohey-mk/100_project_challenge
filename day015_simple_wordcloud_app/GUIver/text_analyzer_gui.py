# text_analyzer_gui.py

### === Imports ===
from janome.tokenizer import Tokenizer

# Text analyzer
def text_analyzer_gui(csv_text_data, csv_stopwords_gui=None):
    if csv_stopwords_gui is None:
        csv_stopwords_gui = []

    t = Tokenizer()
    words = []
    for sentence in csv_text_data:
        tokens = t.tokenize(sentence)
        for token in tokens:
            word = token.surface
            part_of_speech = token.part_of_speech.split(',')[0]
            if part_of_speech == "名詞" and word not in csv_stopwords_gui:
                words.append(word)
    return words