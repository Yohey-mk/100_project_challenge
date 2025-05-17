# cli.py

### === imports ===


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
    pass

#Delete Notes
def delete_notes(user_notebook):
    pass

#Close app
def close_app():
    exit()

### === App Logics ===
def main():
    user_notebook = []

    while True:
        user_input = input("Choose your option:\n1. Create a new note\n2. Show all notes\n3. Update notes\n4. Delete notes\n5. Close app\nEnter your option: ")
        if user_input == "1":
            user_note = input("Enter your note: ")
            create_new_note(user_note,user_notebook)
        elif user_input == "2":
            show_all_notes(user_notebook)
        elif user_input == "3":
            update_notes(user_notebook)
        elif user_input == "4":
            delete_notes(user_notebook)
        elif user_input == "5":
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