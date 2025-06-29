# show_all_notes.py
import flet as ft

def show_all_notes(page, my_schedule):

    filtered_schedule = my_schedule.copy()
    date_input_field = ft.TextField(label="YYYY-MM-DD")
    schedule_list = ft.Column()

    def search_by_date(e):
        nonlocal filtered_schedule
        date_input = date_input_field.value.strip()
        if date_input:
            filtered_schedule = [note for note in my_schedule if note["date"] == date_input]
        else:
            filtered_schedule = my_schedule.copy()
        refresh_schedule_list()

    def refresh_schedule_list():
        schedule_list.controls.clear()
        for idx, schedule in enumerate(filtered_schedule):
            card = ft.Card(
                content = ft.Container(
                    content = ft.Column([
                    ft.Text(f"{idx + 1}. {schedule['date']} {schedule['time']} {schedule['title']}"),
                    ft.Text(f"{schedule['detail']}")
                    ])
                )
            )
            schedule_list.controls.append(card)
            page.update()

    refresh_schedule_list()
    date_search_button = ft.ElevatedButton(text="Search", on_click=search_by_date)


    return ft.Column([date_input_field,
                      date_search_button,
                      ft.Divider(),
                      schedule_list])