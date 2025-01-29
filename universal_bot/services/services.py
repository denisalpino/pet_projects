from random import choice, randint


def get_random_item() -> int:
    """Функция генерирует выбор бота в игре камень, ножницы, бумага"""
    return choice(['rock', 'paper', 'scissors'])


def get_winner(user_choice: str, bot_choice: str) -> str:
    """Функция определяет победителя в игре камень, ножницы, бумага"""
    rules = {'rock': 'scissors',
             'scissors': 'paper',
             'paper': 'rock'}
    if user_choice == bot_choice:
        return 'draw'
    elif rules[user_choice] == bot_choice:
        return 'win'
    return 'lose'


def get_random_number(start: int=1, end: int=100) -> int:
    """Функция генерирует загаданное число бота в игре Числовая угадайка"""
    return randint(start, end)