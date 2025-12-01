import random


# Вопросы, которые будем задавать
questions = [
        ('2^6 = ...', 64),
        ('3! = ...', 6),
        ('0^0 = ...', 1),
        ('5! = ...', 120),
        ('C\', где C -  const = ...', 0),
    ]

def main(questions):
    wrong = 3
    score = 0
    
    shuffled_questions = random.sample(questions, len(questions))
    
    for question, correct_answer in shuffled_questions:
        print('--------Математическая викторина.--------\nНапиши правильный ответ\n')
        print(question)
        user_answer = float(input('Введите число: '))
        
        if user_answer == correct_answer:
            print('(+1) Верно!\n')
            score += 1
        else:
            wrong -= 1
            print(f'(-1) Неверно! Осталось попыток: {wrong}\n')
            if wrong == 0:
                print('\nИгра окончена!')
                return f'Ваш результат: {score} баллa(-ов)'
    
    return f'Вы заработали {score} баллa(-ов)!'


if __name__ == "__main__":
    print(main(questions))
