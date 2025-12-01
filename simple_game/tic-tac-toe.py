import random
import time


PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

def create_board():
    """Создание игрового поля 3 на 3"""
    return [[EMPTY for _ in range(3)] for _ in range(3)]


def display_board(board):
    """Отображение игрового поля в терминале"""
    print("\n   | 1 | 2 | 3 |")
    print("---------------")
    for i, row in enumerate(board):
        print(f" {i+1} | {' | '.join(row)} |")
        print("---------------")


def is_board_full(board):
    """
    Проверка пустых клеток. Возвращает True,
    только если все поля заполнены
    """
    for row in board:
        if EMPTY in row:
            return False
    return True


def player_move(board, player):
    """Обработка хода игрока"""
    while True:
        try:
            print(f"\nХод игрока {player}")
            row = int(input("Введите номер строки (1-3): "))
            col = int(input("Введите номер столбца (1-3): "))
            
            if 1 <= row <= 3 and 1 <= col <= 3:
                row_index = row - 1
                col_index = col - 1
                if board[row_index][col_index] == EMPTY:
                    board[row_index][col_index] = player
                    return
                else:
                    print("Эта клетка уже занята! Попробуйте другую.")
            else:
                print("Введите числа от 1 до 3!")
        except ValueError:
            print("Пожалуйста, введите числа!")


def computer_move(board, computer):
    """Ход компьютера"""
    # Сначала ищем выигрышный ход
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = computer
                if check_winner(board, computer):
                    return
                board[i][j] = EMPTY
    
    # Блокируем выигрыш игрока
    player = PLAYER_X if computer == PLAYER_O else PLAYER_O
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = player
                if check_winner(board, player):
                    board[i][j] = computer
                    return
                board[i][j] = EMPTY
    
    # Если нет срочных ходов, ходим случайно
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                empty_cells.append((i, j)) # Собираем свободные клетки
    
    if empty_cells:
        row, col = random.choice(empty_cells) # Выбираем случайную
        board[row][col] = computer            # Делаем ход


def check_winner(board, player):
    """Проверка победы"""
    # Проверяем строки
    for row in board:
        if all(cell == player for cell in row):
            return True
    
    # Проверяем столбцы
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    
    # Проверяем диагонали
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    
    return False


def main():
    board = create_board()
    current_player = PLAYER_X # Первый ход у игрока

    print("Добро пожаловать в Крестики-нолики!")
    print("Для хода вводите координаты: строка (1-3) и столбец (1-3)")
    
    while True:
        display_board(board)

        if current_player == PLAYER_X:
            player_move(board, PLAYER_X)
        else:
            print("\nКомпьютер думает...")
            time.sleep(2)
            computer_move(board, PLAYER_O)
        
        # Проверяем окончания игры
        if check_winner(board, current_player):
            display_board(board)
            if current_player == PLAYER_X:
                print("\n-----🎉 Поздравляю! Вы победили!-----")
            else:
                print("\n-----💻 Компьютер победил!-----")
            break
        
        # Проверяем ничью
        if is_board_full(board):
            display_board(board)
            print("\n-----🤝 Ничья!-----")
            break
        
        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X

if __name__ == "__main__":
    main()
