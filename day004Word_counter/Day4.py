#Day4 Word counter
from collections import Counter
user_input = input("Write whatever you'd like!: ")

if user_input.strip() == "":
    print("Empty input.")
else:
    word_list = user_input.split()
    word_num = len(word_list)
    word_character_num_without_spaces = sum(len(word) for word in word_list)
    word_character_num_with_spaces = len(user_input)
    word_average = round(word_character_num_without_spaces / word_num, 2)
    longest_word = max(word_list, key=len)
    shortest_word = min(word_list, key=len)
    word_count = Counter(word_list)
    if word_num == 1:
        print(f"Word count: 1. Total character count: {word_character_num_without_spaces}")
    else:
        print(f"Word count: {word_num}")
        print(f"Total character count: {word_character_num_without_spaces}")
        print(f"Total character count with space: {word_character_num_with_spaces}")
        print(f"Word character average: {word_average}")
        print(f"Longest word: {longest_word}")
        print(f"Shortest word: {shortest_word}")
        for word, count in word_count.items():
            print(f"{word}: {count}")