from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

import services
import keyboards
from lexicon import LEXICON_RU
from database import User, Games


router = Router()


# Обработчик команды \start
@router.message(CommandStart())
async def process_start_command(message: Message, UsersStorage: dict[int, User]):
    if message.from_user.id not in UsersStorage:
        UsersStorage[message.from_user.id] = User()

    await message.answer(
        text=LEXICON_RU['/start']
    )


# Обработчик команды \help
@router.message(Command(commands='help'))
async def process_help_command(message: Message, UsersStorage: dict[int, User]):
    await message.answer(
        text=LEXICON_RU['/help']
    )


# Обработчик команды \play
@router.message(Command(commands='play'))
async def process_play_command(message: Message | CallbackQuery, UsersStorage: dict[int, User]):
    user = UsersStorage[message.from_user.id]

    if isinstance(message, CallbackQuery):
        await message.message.delete()
        message = message.message

    if user.is_playing:
        await message.answer(
            text=LEXICON_RU[user.current_game.value]['impossible_answer']
        )
    else:
        user.is_playing = True

        await message.answer(
            text=LEXICON_RU['/play'],
            reply_markup=keyboards.games_kb
        )


# Обработчик команды \roles
@router.message(Command(commands='roles'))
async def process_roles_command(message: Message, UsersStorage: dict[int, User]):
    user = UsersStorage[message.from_user.id]

    # Если пользователь сейчас играет, выводим правила текущей игры, иначе же отправляем клавиатуру с выбором игры
    if user.current_game:
        await message.answer(
            text=LEXICON_RU[user.current_game.value]['/roles']
            )
    else:
        await message.answer(
            text=LEXICON_RU['/roles'],
            reply_markup=keyboards.roles_kb
        )


# Обрабатываем нажатие на кнопку для отображения правил конкретной игры
@router.callback_query(F.data.in_(['rock_paper_scissors_roles', 'number_guessing_roles']))
async def describe_roles(callback: CallbackQuery, UsersStorage: dict[int, User]):
    game = callback.data.replace('_roles', '')

    await callback.answer() # Убираем знак часов
    await callback.message.answer(
        text=LEXICON_RU[game]['/roles']
    )
    await callback.message.delete()


# Обработчик команды \cancel
@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message, UsersStorage: dict[int, User]):
    user = UsersStorage[message.from_user.id]

    if user.is_playing:
        if user.current_game == Games.RockPaperScissors:
            await message.answer(
            text=LEXICON_RU['rock_paper_scissors']['impossible_answer']
            )
        else:
            user.current_game = None
            user.is_playing = False

            await message.answer(
            text=LEXICON_RU['/cancel']
            )
    else:
        await message.answer(
            text=LEXICON_RU['is_not_playing_yet']
        )


# Обработчик команды \stat
@router.message(Command(commands='stat'))
async def process_stat_command(message: Message, UsersStorage: dict[int, User]):
    user = UsersStorage[message.from_user.id]

    # Если пользователь сейчас играет, выводим статистику по текущей игре, иначе же отправляем клавиатуру с выбором игры
    if user.current_game:
        if user.current_game == Games.NumberGuessing:
            profile = user.number_guessing
        elif user.current_game == Games.RockPaperScissors:
            profile = user.rock_paper_scissors

        win_rate = round(100 * profile.wins / profile.total_games) if profile.total_games else 0

        await message.answer(
            text=LEXICON_RU[user.current_game.value]['/stat'].format(
                profile.total_games,
                profile.wins,
                win_rate
            )
        )
    else:
        await message.answer(
            text=LEXICON_RU['/stat'],
            reply_markup=keyboards.stat_kb
        )

# Обрабатываем нажатие на кнопку для отображения статистики по конкретной игре
@router.callback_query(F.data.in_(['rock_paper_scissors_stat', 'number_guessing_stat']))
async def describe_stat(callback: CallbackQuery, UsersStorage: dict[int, User]):
    user = UsersStorage[callback.from_user.id]
    game = callback.data.replace('_stat', '')

    if game == Games.NumberGuessing.value:
        profile = user.number_guessing
    elif game == Games.RockPaperScissors.value:
        profile = user.rock_paper_scissors

    win_rate = round(100 * profile.wins / profile.total_games) if profile.total_games else 0

    await callback.answer() # Убираем знак часов
    await callback.message.answer(
        text=LEXICON_RU[game]['/stat'].format(
            profile.total_games,
            profile.wins,
            win_rate
        )
    )
    await callback.message.delete()


# Обрабатываем нажатие на кнопку 'Камень🗿, ножницы✂️, бумага📃'
@router.callback_query(F.data == 'rock_paper_scissors')
async def start_rock_paper_scissors_game(callback: CallbackQuery, UsersStorage: dict[int, User]):
    user = UsersStorage[callback.from_user.id]

    user.is_playing = True
    user.current_game = Games.RockPaperScissors

    await callback.answer() # Убираем знак часов
    await callback.message.answer(
        text=LEXICON_RU[user.current_game.value]['welcome'],
        reply_markup=keyboards.rock_paper_scissors_kb
    )
    await callback.message.delete()


# Обрабатываем нажатие на одну из кнопок 'Камень🗿', 'Бумага📃', 'Ножницы✂️'
@router.callback_query(F.data.in_(LEXICON_RU['rock_paper_scissors']['buttons']))
async def process_rock_paper_scissors_answer(callback: CallbackQuery, UsersStorage: dict[int, User]):
    user = UsersStorage[callback.from_user.id]

    bot_item = services.get_random_item() # Генерируем случайный ответ
    result = services.get_winner(callback.data, bot_item) # Определяем победителя

    bot_item = LEXICON_RU['rock_paper_scissors']['buttons'][bot_item]

    if result == 'win':
        user.rock_paper_scissors.wins += 1
    user.rock_paper_scissors.total_games += 1

    await callback.answer() # Убираем знак часов
    await callback.message.answer(
        text=LEXICON_RU['rock_paper_scissors'][result].format(bot_item),
        reply_markup=keyboards.yes_no_kb
    )
    await callback.message.delete()


# Обрабатываем нажатие на кнопку 'Числовая угадайка🔢'
@router.callback_query(F.data == 'number_guessing')
async def start_number_guessing_game(callback: CallbackQuery, UsersStorage: dict[int, User]):
    user = UsersStorage[callback.from_user.id]

    user.is_playing = True
    user.current_game = Games.NumberGuessing
    user.number_guessing.attempts = 7
    user.number_guessing.secret_number = services.get_random_number(1, 100)

    await callback.answer() # Убираем знак часов
    await callback.message.answer(text=LEXICON_RU[user.current_game.value]['welcome'])
    await callback.message.delete()


# Обрабатываем сообщения полностью состоящие из чисел
@router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_guessing_answer(message: Message, UsersStorage: dict[int, User]):
    user = UsersStorage[message.from_user.id]

    if user.current_game == Games.NumberGuessing:
        # Логика обработки ответа, если текущая игра пользователя Числовая угадайка
        curr_num = int(message.text)

        if curr_num == user.number_guessing.secret_number:
            user.is_playing = False
            user.number_guessing.wins += 1
            user.number_guessing.total_games += 1

            await message.answer(
                text=LEXICON_RU['number_guessing']['win'],
                reply_markup=keyboards.yes_no_kb
            )
        else:
            user.number_guessing.attempts -= 1

            if not user.number_guessing.attempts:
                user.is_playing = False
                user.number_guessing.total_games += 1

                await message.answer(
                    text=LEXICON_RU['number_guessing']['lose'].format(user.number_guessing.secret_number),
                    reply_markup=keyboards.yes_no_kb
                )
            else:
                more_or_less = ("меньше", "больше")[curr_num < user.number_guessing.secret_number]

                await message.answer(
                    text=LEXICON_RU['number_guessing']['next_try'].format(more_or_less, user.number_guessing.attempts)
                )
    elif not user.is_playing:
        # Отправляем ответ если пользователь еще не играет
        await message.answer(
            text=LEXICON_RU['is_not_playing_yet']
        )
    else:
        # Отправляем сообщение о невозможном ответе для конкретной игры, если пользователь играет в другую игру
        await message.answer(
            text=LEXICON_RU[user.current_game.value]['impossible_answer']
        )

# Обрабатываем нажатие на инлайн-кнопку 'Давай😎'
@router.callback_query(F.data == 'Давай😎')
async def process_positive_answer(callback: CallbackQuery, UsersStorage: dict[int, User]):
    user = UsersStorage[callback.from_user.id]

    await callback.answer() # Убираем знак часов

    if user.current_game == Games.RockPaperScissors:
        await start_rock_paper_scissors_game(callback, UsersStorage)
    elif user.current_game == Games.NumberGuessing:
        await start_number_guessing_game(callback, UsersStorage)
    else:
        await process_play_command(callback, UsersStorage)

# Обрабатываем нажатие на инлайн-кнопку 'Не хочу☹️'
@router.callback_query(F.data == 'Не хочу☹️')
async def process_negative_answer(callback: CallbackQuery, UsersStorage: dict[int, User]):
    user = UsersStorage[callback.from_user.id]

    user.is_playing = False
    user.current_game = None

    await callback.answer() # Убираем знак часов
    await callback.message.answer(
        text=LEXICON_RU['disagreement']
    )
    await callback.message.delete()

# Обрабатывем любые сообщения не прошедшие предыдущие хэндлеры
@router.message()
async def process_other_answers(message: Message, UsersStorage: dict[int, User]):
    user = UsersStorage[message.from_user.id]

    if user.is_playing:
        await message.answer(
            text=LEXICON_RU[user.current_game.value]['impossible_answer']
        )
    else:
        await message.answer(
            text=LEXICON_RU['misunderstanding']
        )