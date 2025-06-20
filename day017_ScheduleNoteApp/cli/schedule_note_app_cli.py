# schedule_note_app_cli.py

### === Imports ===
# data strorage
import json
import os
import sys
from datetime import datetime


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

# Date input validation
def date_input_validation(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
# Get valid date
def get_valid_date():
    while True:
        date_input = input("Enter a date(yyyy-mm-dd) *enter q to quit: ")
        if date_input.lower() == "q":
            return None
        elif date_input_validation(date_input):
            return date_input
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")

# Search a specific date
def search_by_date(notebook, date_input):
    if not notebook:
        print("No notebook found.")
        return
    
    found_notes = [note for note in notebook if note["date"] == date_input]

    if not found_notes:
        print("No notes found for that date.\n")
    else:
        print(f"\nNotes for {date_input}:")
        for i, note in enumerate(found_notes, start=1):
            print(f"{i}. {note['date']} - {note.get('time', '')}")
            print(f"    Title: {note['title']}\n")

# Edit notes from the notebook

def edit_notes(notebook):
    if not notebook:
        print("No notebook found.")
        return
    
    # Select date to edit
    date_to_edit = input("Enter a date to edit(YYYY-MM-DD): ")
    found_notes = [note for note in notebook if note["date"] == date_to_edit]

    if not found_notes:
        print("No notes found for that date.\n")
    else:
        # Let the user to choose edit / delete
        user_choice = input("Enter 'E' to edit, 'D' to delete note: ")

        if user_choice.upper() == "E":
            for i, note in enumerate(found_notes, start=1):
                print(f"{i}. {note['title']}")
            notes_to_edit = input("Which one to edit? Enter q to quit: ")
            if notes_to_edit.lower() == "q":
                print("Canceled.\n")
                return
            elif notes_to_edit.isdigit():
                number_to_edit = int(notes_to_edit) - 1
                if 0 <= number_to_edit < len(found_notes):
                    current_note = found_notes[number_to_edit]
                    print(current_note) # 選んだ番号のノートを表示できている = ここまでちゃんと動作している。
                    new_date = input("Enter a new date(YYYY-MM-DD): ")
                    new_title = input("Enter a new title: ")
                    new_detail = input("Enter a new content: ")
                    if new_date:
                        current_note['date'] = new_date
                    if new_title:
                        current_note['title'] = new_title
                    if new_detail:
                        current_note['detail'] = new_detail
                    print("Notes updated!\n")
                else:
                    print("Invalid note number")

        elif user_choice.upper() == "D":
            for i, note in enumerate(found_notes, start=1):
                print(f"{i}. {note['title']}")
            notes_to_edit = input("Which one to delete? Enter q to quit: ")
            if notes_to_edit.lower() == "q":
                print("Canceled.\n")
                return
            elif notes_to_edit.isdigit():
                number_to_delete = int(notes_to_edit) - 1
                if 0 <= number_to_delete < len(found_notes):
                    note_to_delete = found_notes[number_to_delete]
                    notebook.remove(note_to_delete)
                    print(f"You have deleted {note_to_delete["title"]}\n")

### === App Logics ===
def main():
    notebook = load_notebook()

    # show options
    while True:
        user_choice = input("1. Add new schedule/note\n2. Show all schedule\n3. Show all notes\n4. Search notes by date\n5. Edit notes\n6. End program\nSelect your choice: ")

    # if分岐
        if user_choice == "1": # Must have: date, time(optional), title, details(optional)
            date_input = get_valid_date()
            if date_input is None:
                continue
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
            date_input = get_valid_date()
            if date_input is None:
                continue
            search_by_date(notebook, date_input)
        elif user_choice == "5":
            edit_notes(notebook)
            save_notebook(notebook)
        elif user_choice == "6":
            exit()
        else:
            print("Invalid input. Please select 1 - 6.\n")

### === Run App ===
if __name__ == "__main__":
    main()

### === Notes ===
