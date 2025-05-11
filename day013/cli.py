# cli.py
# === Imports ===


# ===Helper Functions ===
def get_user_input():
    item_input = input("Enter an item: ")
    item_expense = float(input("Enter an expense: "))
    return item_input, item_expense

# Add, Update, Show, Quitは、GUIでいうところのメニュー画面。get_user_inputは、Addの内側のシステム部分。
def update_list():
    pass

#mainの中でf文書いたほうがむしろシンプルかも？
#def show_updated_list():
#    pass

def quit_app():
    exit()
# === App Logics ===
def main():
    expense_book = []

    while True:
        def user_options():
            user_choice = input("Choose your option: \na.Add to list\nb.Update list\nc.Show current list\nd.Quit\nYour option: ").lower()
            if user_choice == "a":
                while True:
                    item, expense = get_user_input()
                    expense_book.append((item, expense))
                    print(f"Current Expense book: {expense_book}")
                    add_more = input("Add more stuff? y/n: ")
                    if add_more == "y":
                        continue
                    else:
                        break
            elif user_choice == "b":
                update_list()
            elif user_choice == "c":
                if len(expense_book) == 0:
                    print("No items to show.\n")
                else:
                    print(f"Current Expense book: {expense_book}\n")
            elif user_choice == "d":
                quit_app()
            else:
                print("Enter a valid option.")
        user_options()
# === UI Components ===


# === UI Interfaces ===
if __name__ == '__main__':
    main()

# === Run App ===


# === Notes ===

