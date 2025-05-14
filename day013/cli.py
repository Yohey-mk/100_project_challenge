# cli.py
# === Imports ===


# ===Helper Functions ===
def get_user_input():
    date = input("Enter the date (yyyy-mm-dd): ")
    item = input("Enter an item: ")
    expense = float(input("Enter an expense: "))
    return {"date": date, "item": item,"expense": expense}

# Add, Update, Show, Quitは、GUIでいうところのメニュー画面。get_user_inputは、Addの内側のシステム部分。
def update_list(expense_book):
    show_updated_list(expense_book)
    try:
        task_number = int(input("Enter the number of the task you want to modify: "))
        if task_number < 1 or task_number > len(expense_book):
            print("Invalid task number.\b")
            return
    except ValueError:
        print("Please enter a valid number.\n")
        return
    
    entry = expense_book[task_number - 1] #実際のリストは0から始まるので、-1する

    print("Which field do you want to update?")
    print("1. Date 2. Item 3. Expense 4. All")
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        entry["date"] = input("Enter the new date (yyyy-mm-dd): ")
    elif choice == "2":
        entry["item"] = input("Enter the new item: ")
    elif choice == "3":
        try:
            entry["expense"] = float(input("Enter the new expense: "))
        except ValueError:
            print("Invalid number entered.")
            return
    elif choice == "4":
        entry.update(get_user_input())
    else:
        print("Invalid option.")
        return
    print("\n*** Task updated successfully! ***\n")
    show_updated_list(expense_book)

#mainの中でf文書いたほうがむしろシンプルかも？
def show_updated_list(expense_book):
    for i, entry in enumerate(expense_book, start=1):
        print(f"{i}. {entry['date']} - {entry['item']}: ¥{entry['expense']}")

def user_options(expense_book):
    user_choice = input("Choose your option: \na.Add to list\nb.Update list\nc.Show current list\nd.Quit\nYour option: ").lower()
    if user_choice == "a":
        while True:
            expense_book.append(get_user_input()) #get_user_input()で辞書を返していて、それをそのままappendしている
            for i, entry in enumerate(expense_book, start=1):
                print(f"{i}. {entry['date']} - {entry['item']}: JPY{entry['expense']}")
            add_more = input("Add more stuff? y/n: ").lower()
            if add_more != "y":
                break    
    elif user_choice == "b":
        update_list(expense_book)
    elif user_choice == "c":
        if len(expense_book) == 0:
            print("No items to show.\n")
        else:
            show_updated_list(expense_book=expense_book)
            total = sum(entry["expense"] for entry in expense_book)
            print(f"Total Expenses: {total} yen\n")
    elif user_choice == "d":
        quit_app()
    else:
        print("Enter a valid option.")

def quit_app():
    exit()
# === App Logics ===
def main():
    expense_book = []

    while True:
        user_options(expense_book)
# === UI Components ===


# === UI Interfaces ===
if __name__ == '__main__':
    main()

# === Run App ===


# === Notes ===

