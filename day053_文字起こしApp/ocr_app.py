# ocr_app.py

import flet as ft
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def extract_text(image_path):
    img = Image.open(image_path)

    text = pytesseract.image_to_string(img, lang='jpn')
    return text

# debug用
# print(extract_text("sample.png"))

def main(page: ft.Page):
    page.title = "OCR Scrapbook"
    page.window.height = 700
    page.window.width = 600

    # UI Component
    # text field to show extracted text
    result_text = ft.TextField(
        multiline=True,
        read_only=True,
        min_lines=10,
        expand=True,
        hint_text="解析したテキストがここに表示されます"
    )

    # pic preview
    image_preview = ft.Image(src="", width=300, height=200, fit=ft.BoxFit.CONTAIN, visible=False)

    # FilePicker
    def read_file(page: ft.Page):
        setup_text = ft.Text()
        file_picker = ft.FilePicker()
        page.services.append(file_picker)
        async def open_file_picker(e: ft.Event[ft.Button]):
            files = await file_picker.pick_files(allow_multiple=True)
            try:
                f = files[0]
                selected_file_path = f.path
                image_preview.src = selected_file_path
                image_preview.visible = True
                result_text.value = "OCR処理中..."
                setup_text.value = ""
                page.update()
            except Exception:
                setup_text.value = "Canceled to load file(s)."
            try:
                extract_text(selected_file_path)
                img = Image.open(selected_file_path)
                text = pytesseract.image_to_string(img, lang='jpn')
                result_text.value = text
                page.update()
            except Exception as err:
                setup_text.value = f"Failed to load file(s): {err}"
            page.update()
        open_button = ft.Button(
            content=ft.Text("Open file(s)"),
            on_click=open_file_picker,
        )
        return ft.Column(controls=[open_button, setup_text])
    open_file_button = read_file(page)

    page.add(
        open_file_button,
        image_preview,
        result_text
    )

ft.run(main)