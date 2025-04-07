#Day 5 To-Do List App
task_list = []

def display_tasks():
    if not task_list:
        print("No tasks available.")
    else:
        print("-------------")
        for index, task in enumerate(task_list, 1):
            print(f"{index}. {task}")
        print("-------------")

while True:
    print("1. Add task")
    print("2. View tasks")
    print("3. Delete task")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter a task: ")
        task_list.append(task)
        print(f"\nAdded!: {task}\n")

    elif choice == "2":
        display_tasks()

    elif choice == "3":
        display_tasks()
        delete_task = input("Enter a task number to delete: ")
        if not delete_task.isdigit():
            print("Invalid input. Please enter a number.")
        elif int(delete_task) < 1 or int(delete_task) > len(task_list):
            print(f"Invalid task number. Please enter a number between 1 and {len(task_list)}.")
        else:
            deleted_task = task_list.pop(int(delete_task) - 1)
            print(f"{deleted_task} has been deleted!")
            print("Updated task list:")
            display_tasks()

    elif choice == "4":
        print("Bye! Have a good day.")
        break
    else:
        print("Invalid input. Please try again.")
