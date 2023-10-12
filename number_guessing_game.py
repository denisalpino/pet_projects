import random

def game():
    right = int(input('Выберете крайнее число: '))

    def is_valid(n):                        # защита от дурака
        if n < 1 or n > right:
            return False
        else:
            return True

    num = random.randint(1, right)
    counter = 0
    while True:
        counter += 1
        n = int(input('Введите предполагаемое число: '))
        if is_valid(n) == False:
            print('А может все-таки попробуем ввести число от 1 до 100?')
        else:
            if n < num:
                print('Ваше число меньше загаданного, попробуйте еще разок')
            elif n > num:
                print('Ваше число больше загаданного, попробуйте еще разок')
            else:
                print('Вы угадали, поздравляем!')
                break
    print('Вам потребовалось всего:', counter, 'попыток, чтобы угадать число!' )


print('Добро пожаловать в числовую угадайку!')
game()

while True:
    answer = input('Хотите попробовать снова: ')
    if answer.lower() in 'даyes':
        game()
    else:
        print('Спасибо, что играли в числовую угадайку. Еще увидимся...')
        break
