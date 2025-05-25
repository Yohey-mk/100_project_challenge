#Day2 project -- 数字当てゲーム
import random
random_number = random.randint(1, 100)
guesses = 0

while True:
    try:
        user_guess = int(input("Enter your guess between 1 - 100: "))
        if 1 <= user_guess <= 100:
            break
        else:
            print("Please enter a number between 1 - 100.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 - 100.")

while True:
    guesses += 1

    if user_guess < 1 or user_guess > 100:
        print("Please enter a number between 1 - 100.")
    elif random_number < user_guess:
        print(f"{user_guess} is bigger than the answer.")
    elif random_number > user_guess:
        print(f"{user_guess} is smaller than the answer.")
    else:
        print(f"Congratulations! The answer is {user_guess}!")
        print(f"You guessed {guesses} times!")
        break

    try:
        user_guess = int(input("Try again: "))
    except ValueError:
        print("Enter a valid number between 1 - 100.")
        user_continue = input("Or if you want to quit the game, enter 'q' to quit: ").lower()
        if user_continue == "q":
            print("End game.")
            exit()
        elif user_continue.isdigit():
            print("Okay, let's continue the game!")
        else:
            print("Did you make a typo?")