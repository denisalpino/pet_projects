import asyncio
import logging
from aiogram import Bot, Dispatcher
import warnings

from configs import load_config, Config
from database import User
from handlers import router


warnings.simplefilter(action='ignore', category=Warning)

logger = logging.getLogger(__name__)


async def main():
    # Конфигурируем логгер
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Начало работы бота')

    # Загружаем конфигурацию бота
    configs: Config = load_config()

    bot = Bot(token=configs.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    # Подключаем роутер к диспетчеру
    dp.include_router(router=router)

    # Создаем "базу данных" с пользовательским данными
    UsersStorage: dict[int, User] = {}

    # Пропускаем накопившиеся апдейты и начинаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, UsersStorage=UsersStorage)


if __name__ == '__main__':
    asyncio.run(main())