#translation_handler.py

### === Import ===
import flet as ft
from argostranslate import translate

#show user input field, translate the text, show the result text by using update() the field value
### === App Logics ===
def translation_handler_ui():
    user_input_field = ft.TextField(label="Enter anything to translate", width=300)
    translate_result = ft.Text(value="", selectable=True, size=16, color=ft.colors.AMBER_500)

    def handle_translate(e):
        installed_languages = translate.get_installed_languages()
        translation_pair = None
        from_lang = None
        to_lang = None

        # 選択言語によってFrom Toを変える
        if dropdown_menu.value == "English":
            for lang in installed_languages:
                if lang.code == "en":
                    from_lang = lang
                elif lang.code == "ja":
                    to_lang = lang
        
        elif dropdown_menu.value == "Japanese":
            for lang in installed_languages:
                if lang.code == "ja":
                    from_lang = lang
                elif lang.code == "en":
                    to_lang = lang

        if from_lang and to_lang:
            translation_pair = from_lang.get_translation(to_lang)
            from_text = user_input_field.value
            translated = translation_pair.translate(from_text)
            translate_result.value = translated
            e.page.update()

    translate_button = ft.ElevatedButton(text="Translate", on_click=handle_translate)
    dropdown_menu = ft.Dropdown(label="From",
                               options=[ft.dropdown.Option("English"),
                                        ft.dropdown.Option("Japanese")],
                                value="English",
                                visible=True)

    return ft.Column(controls=[
        dropdown_menu,
        user_input_field,
        translate_button,
        ft.Text("Translation Result:", weight="bold"),
        translate_result
    ])
