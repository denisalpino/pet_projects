LEXICON_RU = {
    '/start': 'Привет!\nТы попал в универсального бота. '
              'Чтобы управлять мной, тыкни /help, чтобы просмотреть все '
              'доступные способы взаимодействия со мной.',
    '/play': 'Здорово!\n'
             'Выбери и нажми на ту игру, в которую ты хочешь поиграть со мной',
    'is_not_playing_yet': 'Мы сейчас с тобой не играем ни в какую игрую.',
    '/help': 'Доступные команды:\n'
             '/start — Приветствие\n'
             '/help — Вспомогательная информация о командах, чтобы не потеряться\n'
             '/roles — Правила текщий игры\n'
             '/play — Начать игру\n'
             '/cancel — Закончить текущую игру\n'
             '/stat — Показать мою статистику\n\n',
    '/cancel': 'Игра окончена. Увидимся в следующий раз! '
               'Буду с нетерпением ждать новой встречи!',
    'disagreement': 'Жаль :(\n\nЕсли захочешь — я в любое время готов!',
    'misunderstanding': 'К сожалению, я не понимаю, о чем ты...',
    'rock_paper_scissors': {
        'button': 'Камень🗿, ножницы✂️, бумага📃',
        'welcome': 'Что же ты выберешь?',
        'buttons': {
            'rock': 'Камень🗿',
            'paper': 'Бумага📃',
            'scissors': 'Ножницы✂️'
        },
        'win': 'Мой выбор — {}\n\n'
               'Эх! Я проиграл...\n\n'
               'Может сыграем еще?',
        'lose': 'Мой выбор — {}\n\n'
                'Хе-хе-хе! Я победил!\n\n'
                'Не отчаивайся, тебе обязательно '
                'повезет в следующий раз! Может сыграем еще?',
        'draw': 'Мой выбор — {}\n\nНичья!\n\nПродолжим?',
        'impossible_answer': 'Пока мы играем в "камень, ножницы, бумагу" я могу '
                             'реагировать только на нажатия кнопок, '
                             'которые находятся под соответствующим сообщением, '
                             'и команды /stat, /roles и /help',
        '/roles': 'Правила игры:\n\n'
                 '1. Ты выбираешь камень, ножницы или бумагу и нажимаешь на '
                 'соответствующую кнопку, которая отправит в чат твой выбор.\n'
                 '2. Я, одновременно с тобой, тоже делаю выбор и отправляю его '
                 'в чат вместе с исходом игры.\n'
                 '3. Камень побеждает ножницы, ножницы побеждают бумагу, а '
                 'бумага побеждает камень.',
        '/stat': 'Игр сыграно: {}\n'
                 'Побед: {}\n'
                 'Процент побед: {}%'
        },
    'number_guessing': {
        'button': 'Числовая угадайка🔢',
        'welcome': 'Супер!\n\n'
                   'Итак, я загадал число от 1 до 100, теперь у тебя есть 7 '
                   'попыток, чтобы отгадать его, введя правильное число.\n\n'
                   'Как ты думаешь, какое число я загадал?',
        'win': 'Ура!\n\n'
               'Ты угалал число и победил! Поздравляю тебя!\n'
               'Может сыграем еще?',
        'lose': 'У тебя закончились попытки. Не расстраивайся, '
                'ведь ты всегда можешь сыграть еще!\n'
                'А загаданное число было — {}.\n\n'
                'Не хочешь попробовать сыграть еще?',
        'next_try': 'Не угадал. Мое число {}!\n\n'
                    'Количество оставшихся попыток: {}',
        'impossible_answer': 'Пока мы играем в игру "Числовая угадайка" я могу '
                             'реагировать только на числа от 1 до 100 '
                             'и команды /cancel, /stat, /roles и /help',
        '/roles': 'Правила игры:\n\n'
                 '1. Я загадываю число от 1 до 100.\n'
                 '2. У тебя есть 7 попыток, чтобы отгадать число.\n'
                 '3. Чтобы тебе было легче, каждый раз, когда ты будешь отправлять '
                 'предполагаемое число, я буду отвечать тебе больше ли оно загаданного '
                 'или меньше.',
        '/stat': 'Игр сыграно: {}\n'
                 'Побед: {}\n'
                 'Процент побед: {}%'
        },
    'yes_button': 'Давай😎',
    'no_button': 'Не хочу☹️',
    '/roles': 'Правила какой игры ты бы хотел уточнить?',
    '/stat': 'Статистику по какой из игр ты бы хотел уточнить?'
    }