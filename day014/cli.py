# cli.py

### === imports ===
import os
import sys
import json

### === Helper functions ===

#Create New Notes
def create_new_note(user_note,user_notebook):
    user_notebook.append(user_note)
    print(f"Added: {user_note}\n")

#Show all notes
def show_all_notes(user_notebook):
    if not user_notebook:
        print("No notes found.\n")
    else:
        for i, note in enumerate(user_notebook, start=1):
            print(f"{i}: {note}")
        print("")

#Update Notes *include open/modify
def update_notes(user_notebook):
    if not user_notebook: #まずはuser_notebookが空でないかcheck
        print("No notes to update.\n")
        return

    show_all_notes(user_notebook)
    user_pick = input("Pick which one to update(or enter q to go back): ")

    if user_pick.lower() == "q":
        return
    
    try:
        update_number = int(user_pick) - 1
        if 0 <= update_number < len(user_notebook):
            current_note = user_notebook[update_number]
            print(f"Current note: {current_note}\n-----------")
            user_notebook[update_number] = input("Enter new note: ")
            print("Note updated!\n")
        else:
            print("Invalid note number.\n")
    except ValueError:
        print("If you made a typo, try again.")

#Delete Notes
def delete_notes(user_notebook):
    if not user_notebook:
        print("No notes to delete.")
        return
    try:
        show_all_notes(user_notebook)
        user_pick = input("Which one to delete? (enter 'q' to go back): ")

        if user_pick.lower() == "q":
            print("Cancelled.\n")

        elif user_pick.isdigit():
            number_to_delete = int(user_pick) - 1
            if 0 <= number_to_delete < len(user_notebook):
                note_to_delete = user_notebook[number_to_delete]
                print(f"You chose: {note_to_delete}")
                make_sure = input("Are you sure to delete? (y/n): ").lower()
                if make_sure == "y":
                    remove_note = user_notebook.pop(number_to_delete)
                    print(f"Successfully removed {remove_note}.\n")
                else:
                    print("Return to home.\n")
            else:
                print("Invalid input.\n")

    except (ValueError, IndexError):
        print("Invalid input. Please choose a valid number from the list.")
        return

#Save notebook
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys.MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def save_notebook(user_notebook, filename="day14_notebook.json"):
    path = resource_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(user_notebook, f, ensure_ascii=False, indent=2)

def load_notebook(filename="day14_notebook.json"):
    path = resource_path(filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

#Close app
def close_app():
    exit()

### === App Logics ===
def main():
    user_notebook = load_notebook()

    while True:
        user_input = input("Choose your option:\n1. Create a new note\n2. Show all notes\n3. Update notes\n4. Delete notes\n5. Close app\nEnter your option: ")
        if user_input == "1":
            user_note = input("Enter your note: ")
            create_new_note(user_note,user_notebook)
            save_notebook(user_notebook)
        elif user_input == "2":
            show_all_notes(user_notebook)
        elif user_input == "3":
            update_notes(user_notebook)
            save_notebook(user_notebook)
        elif user_input == "4":
            delete_notes(user_notebook)
            save_notebook(user_notebook)
        elif user_input == "5":
            save_notebook(user_notebook)
            close_app()
        else:
            print("Invalid input. Enter 1 - 5.")


### === Run App ===
if __name__ == "__main__":
    main()


### === Notes ===
#✅ 必須機能（CLI）
#	•	ユーザーがメモを入力して保存できる
#	•	複数のメモをリストで管理（メモのタイトルをリスト表示）
#	•	任意のメモを読み込み・編集できる
#	•	JSON形式でデータを保存・読み込み（Day13の復習）

#CLI Interfaceのヒント
#1. 新規メモを作成
#2. 既存メモを一覧表示
#3. メモを開く・編集する
#4. メモを削除する
#5. 終了

#🏁 まとめ：次に進む前にやると面白い追加機能
#	1.	ノートをファイルに保存・読み込み（JSONでやると学習にも最適）
#	2.	ノートの更新機能（user_notebook[index] = new_note）
#	3.	ノートの削除機能（del user_notebook[index]）
#	4.	検索機能（if keyword in note:）
