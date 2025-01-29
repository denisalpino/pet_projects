from dataclasses import dataclass, field
from enum import Enum


# Перечисление списка доступных игр
class Games(Enum):
    RockPaperScissors = 'rock_paper_scissors'
    NumberGuessing = 'number_guessing'


# Профиль пользователя в игре Числовая угадайка
@dataclass(slots=True)
class NumberGuessingPlayer:
    secret_number: int = field(default=None)
    attempts: int = field(default=0)
    total_games: int = field(default=0)
    wins: int = field(default=0)


# Профиль пользователя в игре камень, ножницы, бумага
@dataclass(slots=True)
class RockPaperScissorsPlayer:
    total_games: int = field(default=0)
    wins: int = field(default=0)


# Профиль пользователя
@dataclass(slots=True)
class User:
    is_playing: bool = field(default=False)
    current_game: Games | None = field(default=None)
    number_guessing: NumberGuessingPlayer = field(default_factory=NumberGuessingPlayer)
    rock_paper_scissors: RockPaperScissorsPlayer = field(default_factory=RockPaperScissorsPlayer)