import random


random_num = random.randint(1, 10)

while True:
    text = 'Введите число и поробуйте угадать ответ(или нажать z для выхода): '
    inp_user = input(text)

    if inp_user == 'z':
        print('Вы вышли из игры')
        break

    try:
        num = int(inp_user)
    except ValueError:
        print("Пожалуйста, введите число или 'z' для выхода!")
        continue
        
        
    if num == random_num:
        print('Вы угадали!')
        break
    else:
        print('Поробуйте снова. В следующий раз повезет')
