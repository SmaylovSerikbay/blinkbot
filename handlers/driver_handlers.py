"""
Обработчики для водителей
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.engine import async_session_maker
from database.requests import UserRepository
from keyboards.inline import get_phone_request_keyboard
from locales.translations import get_text

router = Router()


@router.callback_query(F.data == "role_driver")
async def process_driver_role(callback: CallbackQuery, t, telegram_id, user_lang):
    """Обработчик выбора роли водителя"""
    async with async_session_maker() as session:
        # Сохраняем роль
        await UserRepository.update_role(session, telegram_id, "driver")
        
        # Проверяем наличие телефона
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        
        if not user or not user.phone_number:
            # Если телефона нет - запрашиваем
            await callback.message.edit_text(
                t("driver.need_phone")
            )
            await callback.message.answer(
                t("driver.need_phone"),
                reply_markup=get_phone_request_keyboard(user_lang)
            )
        else:
            # Если телефон есть - проверяем верификацию
            if not user.is_verified:
                await callback.message.edit_text(
                    t("driver.need_verification")
                )
            else:
                # Водитель верифицирован - можно создавать поездки
                await callback.message.edit_text(
                    t("driver.create_trip")
                )
        
        await callback.answer()


@router.message(F.contact)
async def process_contact(message: Message, t, telegram_id, user_lang):
    """Обработчик получения контакта (телефона)"""
    contact = message.contact
    phone_number = contact.phone_number
    
    # Если контакт от другого пользователя, игнорируем
    if contact.user_id != telegram_id:
        await message.answer(t("errors.unknown_error"))
        return
    
    async with async_session_maker() as session:
        await UserRepository.update_phone(session, telegram_id, phone_number)
        
        # Убираем клавиатуру
        from aiogram.types import ReplyKeyboardRemove
        await message.answer(
            t("driver.phone_saved"),
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Проверяем верификацию
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if user and not user.is_verified:
            await message.answer(
                t("driver.need_verification")
            )


@router.message(Command("verify"))
async def cmd_verify(message: Message, t, telegram_id, user_lang, state: FSMContext):
    """Команда для начала верификации"""
    async with async_session_maker() as session:
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        
        if not user or user.role != "driver":
            await message.answer(t("errors.unknown_error"))
            return
        
        if user.is_verified:
            await message.answer(t("verification.already_verified"))
            return
        
        if not user.phone_number:
            await message.answer(t("driver.need_phone"))
            return
        
        # Начинаем процесс верификации
        from states.verification_states import VerificationStates
        await state.set_state(VerificationStates.license_photo)
        await message.answer(t("verification.start"))

