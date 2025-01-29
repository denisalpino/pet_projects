from dataclasses import dataclass
from environs import Env


@dataclass(slots=True)
class TgBot:
    token: str


@dataclass(slots=True)
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(TgBot(token=env('BOT_TOKEN')))