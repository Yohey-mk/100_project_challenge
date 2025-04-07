#Day 7 FizzBuzz Game
import sys

def fizzbuzz_bazz(number):
    """FizzBuzzBazzの判定"""
    result = ""
    if number % 3 == 0:
        result += "Fizz"
    if number % 5 == 0:
        result += "Buzz"
    if number % 7 == 0:
        result += "Bazz"
    if number % 3 != 0 and number % 5 != 0 and number % 7 != 0:
        result += "None"
    #上記以外の場合はNoneを選択肢に加え、それを選択すると正解にするようにする
    return result

def calculation():
    player_score = 0
    playing_stage = 1
    def user_guess_new():
        print("\nGuess your answer from the list below. Press Q to quit.")
        print("0:None 1:Fizz 2:Buzz 3:Bazz\n4:FizzBuzz 5:FizzBazz 6:BuzzBazz 7:FizzBuzzBazz")
        user_input = input("Enter: ").lower()
        if user_input == "q" and playing_stage == 1:
            print("Thank you for playing. Hope to see you soon!")
            sys.exit()
        elif user_input == "q":
            print(f"End Game. Your final score: {player_score}. Correct answer rate: {correct_answer_rate:.1f}%")
            print("Thank you for playing. Hope to see you again!")
            sys.exit()
        return user_input

    for number in range(1, 101):
        correct_answer = fizzbuzz_bazz(number)
        print(f"Stage#{playing_stage}. Q. Number: {number}")
        user_answer = user_guess_new()
        playing_stage += 1
        expected_inputs = {
            "fizz": "Fizz", "buzz": "Buzz", "bazz": "Bazz",
            "fizzbuzz": "FizzBuzz", "fizzbazz": "FizzBazz",
            "buzzbazz": "BuzzBazz", "fizzbuzzbazz": "FizzBuzzBazz", "none": "None"
        }
        if user_answer in expected_inputs and expected_inputs[user_answer] == correct_answer:
            print("Correct!")
            player_score += 1
            correct_answer_rate = (player_score / (playing_stage-1)) * 100
        else:
            print(f"Oops! The answer was {correct_answer}.")
            player_score += 0
            correct_answer_rate = (player_score / (playing_stage-1)) * 100
        print(f"Current Score: {player_score}. Correct answer rate: {correct_answer_rate:.1f}%") #これまでの正答率をX％で表示するようにしたらゲーム性がプラスされて面白いかも？
        print("----------")

    print(f"Game set! Your final score: {player_score}")


if __name__ == "__main__":
    calculation()


#3の倍数のときは “Fizz”
    # %で余り0を調べられる
#5の倍数のときは “Buzz”
    # 
#3と5両方の倍数のときは “FizzBuzz”

#それ以外のときは数字をそのまま表示


#--------------------------
#☑7の倍数のときは “Bazz” を追加
#3と7の倍数 → “FizzBazz”
#5と7の倍数 → “BuzzBazz”
#3, 5, 7全ての倍数 → “FizzBuzzBazz”
#my ideas-------------------
#☑earn points
#☑let the user to quit whenever they want
#my notes-------------------
#x回処理を繰り返すというのはfor文をつかう。書き方は,for VARIABLE in range(x, y):という書き方