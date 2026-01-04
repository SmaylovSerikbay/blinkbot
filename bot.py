"""
Основной файл запуска Telegram-бота Blink
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import config
from database.engine import init_db
from middlewares.i18n import I18nMiddleware
from handlers import user_handlers, driver_handlers, verification_handlers


async def main():
    """Точка входа в приложение"""
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Создание бота и диспетчера
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Инициализация БД
    await init_db()

    # Регистрация middleware
    dp.message.middleware(I18nMiddleware())
    dp.callback_query.middleware(I18nMiddleware())

    # Регистрация роутеров
    dp.include_router(user_handlers.router)
    dp.include_router(driver_handlers.router)
    dp.include_router(verification_handlers.router)

    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

