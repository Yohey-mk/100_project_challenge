# translator_app.py

### === Imports ===
from translate import Translator
import sentencepiece as spm

### === Helper Functions ===

### === App Logics ===
def main():
    translator = Translator(to_lang="ja")
    translation = translator.translate("Good morning folks!")
    print(translation)
    print(spm.__version__)

### === Main ===
if __name__ == "__main__":
    main()


