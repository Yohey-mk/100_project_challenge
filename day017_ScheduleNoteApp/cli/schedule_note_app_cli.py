# schedule_note_app_cli.py

### === Imports ===
# data strorage
import json
import os
import sys


### === Helper Functions ===

# save/load data
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys.MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def save_notebook(filename, notebook):
    path = resource_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)

def load_notebook(filename="day17_CLI.json"):
    path = resource_path(filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

### === App Logics ===
def main():
    notebook = load_notebook()

    # show options
    user_choice = input("1. Add new schedule/note\n2. Show all schedule\n3. Show all notes\n4. End program\nSelect your choice: ")

    # if分岐
    if user_choice == "1": # Must have: date, time(optional), title, details(optional)
        date_input = input("Enter a date: ")
        title_input = input("Enter a title: ")
        time_input = input("Enter a time if applicable (n to skip): ")
        if time_input == "n":
            time_input = ""
        detail_input = input("Enter a detail if applicable (n to skip): ")
        if detail_input == "n":
            detail_input = ""
        note = {"date":date_input, "title":title_input, "time":time_input, "detail":detail_input}
        notebook.append(note)
        print(notebook)
    elif user_choice == "2": # Show date, time(if applicable), title
        pass
    elif user_choice == "3": # Show date, time, title, details
        pass
    elif user_choice == "4":
        exit()

### === Run App ===
if __name__ == "__main__":
    main()

### === Notes ===
