# translator_app.py

### === Imports ===
#from translate import Translator
from argostranslate import translate
import sentencepiece as spm

### === Helper Functions ===

### === App Logics ===
def main():
    installed_languages = translate.get_installed_languages()
    translation_pair = None

    for lang in installed_languages:
        if lang.code == "en":
            from_lang = lang
        elif lang.code == "ja":
            to_lang = lang

    if from_lang and to_lang:
            translation_pair = from_lang.get_translation(to_lang)

    if translation_pair:
        text = input("Enter English text: ")
        translated = translation_pair.translate(text)
        print("Japanese translation: ", translated)
    else:
        print("Translation pair (en -> ja) not found. Install the language model.")

### === Main ===
if __name__ == "__main__":
    main()


# Notes
# translateを使っていたときのコード
#    translator = Translator(to_lang="ja")
#    translation = translator.translate("Hello world!")
#    print(translation)

# sentencepieceが使えるとこんなことができるらしい
#	•	サブワード分割（BPEやUnigramモデル）の学習と適用
#	•	日本語テキストの前処理（形態素解析なしでもOK）
#	•	自作の翻訳モデルや要約モデルへの応用
#	•	ファイルベースでトークナイザーを訓練・保存・読み込み など