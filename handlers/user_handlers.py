"""
Обработчики для пользователей
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.engine import async_session_maker
from database.requests import UserRepository
from keyboards.inline import get_language_keyboard, get_role_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, t, user_lang, telegram_id):
    """Обработчик команды /start"""
    async with async_session_maker() as session:
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        
        # Если пользователь существует и у него уже выбран язык
        if user and user.language_code:
            # Показываем меню выбора роли
            await message.answer(
                t("start.choose_role"),
                reply_markup=get_role_keyboard(user_lang)
            )
        else:
            # Если пользователь новый или язык не выбран - показываем выбор языка
            await message.answer(
                t("start.welcome"),
                reply_markup=get_language_keyboard()
            )


@router.callback_query(F.data.startswith("lang_"))
async def process_language_selection(callback: CallbackQuery, t, telegram_id, user_lang):
    """Обработчик выбора языка"""
    lang_code = callback.data.split("_")[1]  # Получаем код языка (ru, kz, uz, en)
    
    if lang_code not in ["ru", "kz", "uz", "en"]:
        await callback.answer("Неверный язык")
        return
    
    async with async_session_maker() as session:
        # Сохраняем или обновляем язык пользователя
        user = await UserRepository.get_or_create(
            session,
            telegram_id,
            language_code=lang_code
        )
        
        if user.language_code != lang_code:
            await UserRepository.update_language(session, telegram_id, lang_code)
        
        # Показываем сообщение о выборе языка и меню ролей
        from locales.translations import get_text
        await callback.message.edit_text(
            get_text("start.language_selected", lang_code)
        )
        await callback.message.answer(
            get_text("start.choose_role", lang_code),
            reply_markup=get_role_keyboard(lang_code)
        )
        await callback.answer()


@router.callback_query(F.data.startswith("role_"))
async def process_role_selection(callback: CallbackQuery, t, telegram_id, user_lang):
    """Обработчик выбора роли"""
    role = callback.data.split("_")[1]  # Получаем роль (driver или passenger)
    
    if role not in ["driver", "passenger"]:
        await callback.answer(t("errors.unknown_error"))
        return
    
    async with async_session_maker() as session:
        # Сохраняем роль пользователя
        await UserRepository.update_role(session, telegram_id, role)
        
        if role == "passenger":
            # TODO: Показ ленты поездок
            await callback.message.edit_text(
                t("passenger.search_trips")
            )
        # Обработка роли driver выполняется в driver_handlers.py через callback "role_driver"
        
        await callback.answer()

