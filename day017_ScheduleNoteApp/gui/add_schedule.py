# add_schedule.py
import flet as ft

def add_schedule(on_submit_handler):
    date_input_field = ft.TextField(label="Date", width=300, hint_text="YYYY-MM-DD")
    time_input_field = ft.TextField(label="Time", width=300, hint_text="Leave blank to skip")
    title_input_field = ft.TextField(label="Title", width=300)
    detail_input_field = ft.TextField(label="Detail", width=300)

    def on_submit(e):
        schedule = {
            'date':date_input_field.value,
            'time':time_input_field.value,
            'title':title_input_field.value,
            'detail':detail_input_field.value}
        on_submit_handler(schedule)
        e.page.update()

    def create_new_schedule(e):
        date_input_field.value = ""
        time_input_field.value = ""
        title_input_field.value = ""
        detail_input_field.value = ""
        e.page.update()

    save_button = ft.ElevatedButton(text="Save new schedule", on_click=on_submit)
    create_new_button = ft.ElevatedButton(text="Create New", on_click=create_new_schedule)

    return ft.Column(controls=[
        date_input_field,
        time_input_field,
        title_input_field,
        detail_input_field,
        ft.Divider(),
        save_button,
        create_new_button
    ])