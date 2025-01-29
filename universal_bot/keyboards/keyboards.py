from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon import LEXICON_RU


# Создаем клавиатуру для выбора игры, где в колбэке
# отправляется 'rock_paper_scissors' или 'number_guessing'.
games_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text=LEXICON_RU['rock_paper_scissors']['button'],
            callback_data='rock_paper_scissors'
        )],
        [InlineKeyboardButton(
            text=LEXICON_RU['number_guessing']['button'],
            callback_data='number_guessing'
        )]
    ],
    resize_keyboard=True
)

# Создаем клавиатуру для выбора игры для вывода правил
roles_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text=LEXICON_RU['rock_paper_scissors']['button'],
            callback_data='rock_paper_scissors_roles'
        )],
        [InlineKeyboardButton(
            text=LEXICON_RU['number_guessing']['button'],
            callback_data='number_guessing_roles'
        )]
    ],
    resize_keyboard=True
)

# Создаем клавиатуру для выбора игры для вывода статистики
stat_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text=LEXICON_RU['rock_paper_scissors']['button'],
            callback_data='rock_paper_scissors_stat'
        )],
        [InlineKeyboardButton(
            text=LEXICON_RU['number_guessing']['button'],
            callback_data='number_guessing_stat'
        )]
    ],
    resize_keyboard=True
)


# Создаем клавиатуру для выбора камня, ножниц или бумаги, где в колбэке
# отправляется 'rock', 'paper' или 'scissors'.
rock_paper_scissors_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=v,
                callback_data=k
            )
            for k, v in LEXICON_RU['rock_paper_scissors']['buttons'].items()
        ]
    ],
    resize_keyboard=True
)

# Создаем кнопки, где в колбэки отправляется сам текст кнопки
yes_button = InlineKeyboardButton(
    text=LEXICON_RU['yes_button'],
    callback_data=LEXICON_RU['yes_button']
)
no_button = InlineKeyboardButton(
    text=LEXICON_RU['no_button'],
    callback_data=LEXICON_RU['no_button']
)

# Настраиваем клавиатуру
yes_no_kb_builder = InlineKeyboardBuilder()
yes_no_kb_builder.row(yes_button, no_button, width=2)

# Клавиатура для продолжения игры
yes_no_kb = yes_no_kb_builder.as_markup(resize_keyboard=True)