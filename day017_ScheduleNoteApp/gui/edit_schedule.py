# edit_schedule.py
import flet as ft
from save_notebook import save_notebook

def edit_schedule(page, my_schedule):
    choose_schedule = ft.TextField(label="Enter schedule # to edit")
    date_search_field = ft.TextField(label="Search by date (YYYY-MM-DD)")
    date_field = ft.TextField(label="YYYY-MM-DD")
    time_field = ft.TextField(label="HH:MM (*Optional)")
    title_field = ft.TextField(label="Title")
    detail_field = ft.TextField(label="Details")

    filtered_schedule = my_schedule.copy()

    schedule_cards = ft.Column()

    def search_by_date(e):
        nonlocal filtered_schedule
        date_input = date_search_field.value.strip()
        if date_input:
            filtered_schedule = [note for note in my_schedule if note["date"] == date_input]
        else:
            filtered_schedule = my_schedule.copy()
        refresh_schedule_cards()

    for idx, schedule in enumerate(my_schedule):
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{idx + 1}. {schedule['date']} - {schedule['title']}"),
                    ft.Text(schedule['detail'])
                ])
            )
        )
        schedule_cards.controls.append(card)

    def refresh_schedule_cards():
        schedule_cards.controls.clear()
        for idx, schedule in enumerate(filtered_schedule):
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"{idx + 1}. {schedule['date']} - {schedule['title']}"),
                        ft.Text(schedule['detail'])
                    ])
                )
            )
            schedule_cards.controls.append(card)
        page.update()

    def load_schedule(e):
        try:
            idx = int(choose_schedule.value) - 1
            if 0 <= len(filtered_schedule):
                schedule = filtered_schedule[idx]
                date_field.value = schedule['date']
                time_field.value = schedule['time']
                title_field.value = schedule['title']
                detail_field.value = schedule['detail']
            else:
                ft.Text("Invalid input.")
        except ValueError:
            ft.Text("Invalid number.")
        page.update()

    def save_updated_schedule(e):
        idx = int(choose_schedule.value) - 1
        if 0 <= idx < len(filtered_schedule):
            original_index = my_schedule.index(filtered_schedule[idx])
            my_schedule[original_index] = {
                'date': date_field.value,
                'time': time_field.value,
                'title': title_field.value,
                'detail': detail_field.value
            }
            save_notebook(my_schedule)
            refresh_schedule_cards()
            ft.Text("Updated!")
            page.update()

    date_search_button = ft.ElevatedButton(text="Seach", on_click=search_by_date)
    load_button = ft.ElevatedButton(text="Load", on_click=load_schedule)
    save_button = ft.ElevatedButton(text="Save", on_click=save_updated_schedule)

    return ft.Column([
        ft.Text("Search schedule by date"),
        date_search_field,
        date_search_button,
        ft.Divider(),
        ft.Text("Select which schedule to edit"),
        choose_schedule,
        load_button,
        date_field,
        time_field,
        title_field,
        detail_field,
        save_button,
        ft.Divider(),
        ft.Text("Current schedule"),
        schedule_cards
    ])

