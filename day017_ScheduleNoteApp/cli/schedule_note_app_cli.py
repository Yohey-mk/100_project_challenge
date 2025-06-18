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

def save_notebook(notebook, filename="day17_CLI.json"):
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
    
# Show Notes
def show_notes(notebook):
    if not notebook:
        print("No notebook found.\n")
    else:
        sorted_notebook = sorted(notebook, key=lambda to_search: to_search["date"])
        for i, note in enumerate(sorted_notebook, start=1):
            print((f"{i}. {note['date']} - {note['title']}"))
        print()

# Show All Notes *Show Notesを参考にできる！
def show_all_notes(notebook):
    if not notebook:
        print("No notebook found.\n")
    else:
        sorted_notebook = sorted(notebook, key=lambda to_search: to_search["date"])
        for i, note in enumerate(sorted_notebook, start=1):
            print((f"{i}. {note['date']} - {note['time']}"))
            print((f"{note['title']}"))
            print((f"{note['detail']}"))
        print()

# Search a specific date
def search_by_date(notebook):
    pass

# Edit notes from the notebook
def edit_notes(notebook):
    pass

### === App Logics ===
def main():
    notebook = load_notebook()

    # show options
    while True:
        user_choice = input("1. Add new schedule/note\n2. Show all schedule\n3. Show all notes\n4. Search notes by date\n5. Edit notes\n6. End program\nSelect your choice: ")

    # if分岐
        if user_choice == "1": # Must have: date, time(optional), title, details(optional)
            date_input = input("Enter a date(yyyy-mm-dd): ")
            title_input = input("Enter a title: ")
            time_input = input("Enter a time if applicable (n to skip): ")
            if time_input == "n":
                time_input = ""
            detail_input = input("Enter a detail if applicable (n to skip): ")
            if detail_input == "n":
                detail_input = ""
            note = {"date":date_input, "title":title_input, "time":time_input, "detail":detail_input}
            notebook.append(note)
            save_notebook(notebook)
            # print(notebook) debug用に使用していたのでコメントアウト
            print("Note saved!")
        elif user_choice == "2": # Show date, title
            show_notes(notebook)
        elif user_choice == "3": # Show date, time, title, details
            show_all_notes(notebook)
        elif user_choice =="4":
            search_by_date(notebook)
        elif user_choice == "5":
            edit_notes(notebook)
        elif user_choice == "6":
            exit()
        else:
            print("Invalid input. Please select 1, 2, 3, or 4.\n")

### === Run App ===
if __name__ == "__main__":
    main()

### === Notes ===
