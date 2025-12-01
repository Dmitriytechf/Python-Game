import random


def play_game():
    choices = ["камень", "ножницы", "бумага"]

    print("Давай сыграем! Камень, ножницы, бумага...\n")

    user_choice = input("Твой выбор(камень/ножницы/бумага): ").lower()
    computer_choice = random.choice(choices)

    print(f"Компьютер выбрал: {computer_choice}")

    result = winner_game(user_choice, computer_choice)
    return "\n" + result


def winner_game(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "------Ничья!------"
    
    winner_choice = {
        "камень": "ножницы",
        "ножницы": "бумага", 
        "бумага": "камень"
    }
    
    if winner_choice[user_choice] == computer_choice:
        return "------Вы выиграли!------"
    else:
        return "------Ты проиграл!------"


if __name__ == "__main__":
    print(play_game())
