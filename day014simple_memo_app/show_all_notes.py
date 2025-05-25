#Show all notes.py
### === Imports ===
import flet as ft

### === Functions ===
def show_all_notes(page, my_notebook,display_column):
    show_all_notes_switch = ft.Switch(label="Show Notes", value=False)

    def on_toggle(e):
        display_column.controls.clear()
        if show_all_notes_switch.value:
            if my_notebook:
                for idx, entry in enumerate(my_notebook):
                    display_column.controls.append(
                        ft.Text(f"{idx + 1}: {entry['title']}")
                    )
                display_column.visible = True
            else:
                display_column.controls.append(ft.Text("No notes available."))
                display_column.visible = True
        else:
            display_column.visible = False
        
        page.update()
    show_all_notes_switch.on_change = on_toggle
    
    display_column.visible = False

    return ft.Column(controls=[show_all_notes_switch, display_column])