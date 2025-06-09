# gen_wordcloud.py

### === Imports ===
from wordcloud import WordCloud
# import matplotlib.pyplot as plt
import flet as ft
import io
import base64

# Generate Wordcloud
def gen_wordcloud(page):
    image_container = ft.Image(visible=False)

    def on_generate_click(e):
        from load_csv_gui import csv_text_data
        from load_stopwords_gui import csv_stopwords_gui
        from text_analyzer_gui import text_analyzer_gui

        words = text_analyzer_gui(csv_text_data, csv_stopwords_gui)

        if not words:
            print("No words to analyze. Please load valid csv files.")
            return

        text = ' '.join(words)
        wc = WordCloud(font_path="/System/Library/Fonts/ヒラギノ角ゴシック W2.ttc",width=800, height=500, background_color="white").generate(text)

        image = wc.to_image()
        buf = io.BytesIO()
        #plt.imshow(wc, interpolation="bilinear")
        #plt.axis("off")
        #plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        #plt.close()
        image.save(buf, format='PNG')
        buf.seek(0)

        base64_img = base64.b64encode(buf.read()).decode('utf-8')
        image_container.src_base64 = base64_img
        image_container.visible = True
        page.update()


    return ft.Column(controls=[
        ft.ElevatedButton(text="Generate Wordcloud", on_click=on_generate_click),
        image_container
    ])