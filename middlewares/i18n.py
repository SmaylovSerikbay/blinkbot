"""
Middleware для поддержки интернационализации (i18n)
"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import async_session_maker
from database.requests import UserRepository
from locales.translations import get_text, DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


class I18nMiddleware(BaseMiddleware):
    """
    Middleware для обработки языков пользователей.
    Добавляет функцию get_text в контекст хендлеров.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Обработка события с добавлением локализации в контекст
        
        Args:
            handler: Следующий обработчик в цепочке
            event: Событие от Telegram
            data: Словарь с данными для обработчика
        """
        # Получаем telegram_id из события
        telegram_id = None
        if hasattr(event, "from_user") and event.from_user:
            telegram_id = event.from_user.id
        elif hasattr(event, "message") and event.message and event.message.from_user:
            telegram_id = event.message.from_user.id
        elif hasattr(event, "callback_query") and event.callback_query and event.callback_query.from_user:
            telegram_id = event.callback_query.from_user.id

        # Определяем язык пользователя
        user_lang = DEFAULT_LANGUAGE

        if telegram_id:
            # Получаем или создаем пользователя в БД
            async with async_session_maker() as session:
                try:
                    user = await UserRepository.get_by_telegram_id(session, telegram_id)
                    
                    # Если пользователь существует и у него есть язык
                    if user and user.language_code:
                        user_lang = user.language_code
                        # Обновляем данные пользователя из Telegram, если они изменились
                        if hasattr(event, "from_user") and event.from_user:
                            user.username = event.from_user.username
                            user.first_name = event.from_user.first_name
                            user.last_name = event.from_user.last_name
                            await session.commit()
                    else:
                        # Если пользователь новый, создаем его
                        if hasattr(event, "from_user") and event.from_user:
                            from_user = event.from_user
                            await UserRepository.get_or_create(
                                session,
                                telegram_id,
                                username=from_user.username,
                                first_name=from_user.first_name,
                                last_name=from_user.last_name,
                                language_code=DEFAULT_LANGUAGE
                            )
                except Exception as e:
                    # В случае ошибки используем дефолтный язык
                    print(f"Error in I18nMiddleware: {e}")

        # Добавляем функцию локализации в контекст
        def t(key: str, lang: str = None) -> str:
            """Получить переведенный текст"""
            return get_text(key, lang or user_lang)

        data["t"] = t
        data["user_lang"] = user_lang
        data["telegram_id"] = telegram_id

        # Передаем управление следующему обработчику
        return await handler(event, data)

