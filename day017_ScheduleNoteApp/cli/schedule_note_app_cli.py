# schedule_note_app_cli.py

### === Imports ===
# data strorage
import json
import os
import sys


### === Helper Functions ===

# save/load data
def resource_path():
    pass

def save_notebook():
    pass

def load_notebook():
    pass

### === App Logics ===
def main():
    user_notebook = load_notebook()

    # show options
    user_choice = input("1. Add new schedule/note\n2. Show all schedule\n3. Show all notes\n4. End program\nSelect your choice: ")

    # if分岐
    if user_choice == "1":
        pass
    elif user_choice == "2":
        pass
    elif user_choice == "3":
        pass
    elif user_choice == "4":
        exit()

### === Run App ===
if __name__ == "__main__":
    main()

### === Notes ===
