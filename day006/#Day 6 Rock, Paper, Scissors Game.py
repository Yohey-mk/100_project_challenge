#Day 6 Rock, Paper, Scissors Game

import random

# ①ユーザーの入力を受け取る関数
def get_user_choice():
    while True:
        user_hand = input("Choose Rock, Paper, Scissors (or Q to quit): ").lower()
        if user_hand in ["rock", "paper", "scissors", "q"]:
            return user_hand
        print("Oops! Invalid choice. Please choose one of the following: rock, paper, scissors. Or press Q to quit.")

# ②試合結果とスコア加算に関する関数
def play_round(user_hand, computer_hand):
    print(f"You chose {user_hand}, Computer chose {computer_hand}.")
    #あいこの場合
    if user_hand == computer_hand:
        print("It's a tie!")
        return 0
    # elifの()内の組み合わせが、in[(),(),()]の中にあるかチェックし、あればあなたの勝ちと表示
    elif(user_hand, computer_hand) in [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")]:
        print("You win!")
        return 1
    # それ以外の組み合わせ＝負け手なので、You loseと表示
    else:
        print("You lose...")
        return -1

# ③ゲームの流れと構成（この関数の中で①と②を呼び出す）
def main():

    options = ["rock", "paper", "scissors"]
    player_score = 0
    computer_score = 0
    game_stages = 1

    # ユーザーに対戦回数を尋ねる
    while True:
        try:
            number_of_rounds = int(input("How many rounds would you like to play?\n Enter: "))
            if number_of_rounds > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    for _ in range(number_of_rounds):
        user_hand = get_user_choice()
        if user_hand == "q":
            if game_stages == 1:
                print("Alright! Ending the game. Have a nice day!")
                break
            elif game_stages >= 2:
                print(f"Alright! Ending the game.\nYour score was: {player_score} and Computer score was: {computer_score}.")
                break

        computer_hand = random.choice(options)
        game_result = play_round(user_hand, computer_hand)
        game_stages += 1

        if game_result == 1:
            player_score += 1
        elif game_result == -1:
            computer_score += 1
        print(f"Score: You {player_score} - Computer {computer_score}\n")

    if game_stages > 1:
        if player_score > computer_score:
            print("You won the game!")
        elif player_score < computer_score:
            print("You lost the game...")
        elif player_score == computer_score:
            print("It's a draw!")
    else:
        print("Hope to see you again!")

if __name__ == "__main__":
    main()
