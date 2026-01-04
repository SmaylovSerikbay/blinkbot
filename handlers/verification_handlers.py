"""
Обработчики для верификации водителей
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from database.engine import async_session_maker
from database.requests import UserRepository
from states.verification_states import VerificationStates
from config import config
from locales.translations import get_text
from keyboards.inline import get_admin_verification_keyboard

router = Router()


@router.message(VerificationStates.license_photo, F.photo)
async def process_license_photo(message: Message, t, telegram_id, user_lang, state: FSMContext):
    """Обработка фото прав"""
    photo = message.photo[-1]  # Берем фото наибольшего размера
    file_id = photo.file_id
    
    # Сохраняем file_id в состояние
    await state.update_data(license_photo_id=file_id)
    
    # Переходим к следующему шагу
    await state.set_state(VerificationStates.car_photo)
    await message.answer(t("verification.license_received"))


@router.message(VerificationStates.car_photo, F.photo)
async def process_car_photo(message: Message, t, telegram_id, user_lang, state: FSMContext):
    """Обработка фото машины"""
    photo = message.photo[-1]
    car_file_id = photo.file_id
    
    # Получаем данные из состояния
    data = await state.get_data()
    license_photo_id = data.get("license_photo_id")
    
    async with async_session_maker() as session:
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        
        if not user:
            await message.answer(t("errors.unknown_error"))
            await state.clear()
            return
        
        # Сохраняем фото машины
        await UserRepository.update_car_photo(session, telegram_id, car_file_id)
        
        # Отправляем заявку администратору
        admin_id = config.get_admin_id()
        if not admin_id:
            await message.answer(t("errors.admin_not_configured") or "Администратор не настроен. Обратитесь к разработчику.")
            await state.clear()
            return
        admin_text = get_text(
            "admin.verification_request",
            user_lang
        ).format(
            name=user.first_name or "Не указано",
            username=user.username or "нет",
            phone=user.phone_number or "Не указан",
            user_id=telegram_id
        )
        
        try:
            # Отправляем фото прав администратору
            bot = message.bot
            
            await bot.send_photo(
                chat_id=admin_id,
                photo=license_photo_id,
                caption=admin_text
            )
            
            # Отправляем фото машины
            await bot.send_photo(
                chat_id=admin_id,
                photo=car_file_id,
                caption=f"Автомобиль пользователя {telegram_id}",
                reply_markup=get_admin_verification_keyboard(telegram_id)
            )
            
            await message.answer(t("verification.car_received"))
        except Exception as e:
            print(f"Error sending to admin: {e}")
            await message.answer(t("errors.unknown_error"))
        
        await state.clear()


@router.callback_query(F.data.startswith("admin_verify_"))
async def process_admin_verification(callback: CallbackQuery, t, telegram_id):
    """Обработка решения администратора по верификации"""
    # Проверяем, что это администратор
    admin_id = config.get_admin_id()
    if admin_id and telegram_id != admin_id:
        await callback.answer("Доступ запрещен", show_alert=True)
        return
    
    # Парсим callback_data: admin_verify_approve_{user_id} или admin_verify_reject_{user_id}
    parts = callback.data.split("_")
    action = parts[2]  # approve или reject
    driver_id = int(parts[3])
    
    async with async_session_maker() as session:
        user = await UserRepository.get_by_telegram_id(session, driver_id)
        
        if not user:
            await callback.answer("Пользователь не найден", show_alert=True)
            return
        
        driver_lang = user.language_code
        
        if action == "approve":
            # Одобряем верификацию
            await UserRepository.update_verification(session, driver_id, True)
            
            # Отправляем уведомление водителю
            try:
                bot = callback.bot
                
                await bot.send_message(
                    chat_id=driver_id,
                    text=get_text("verification.approved", driver_lang)
                )
            except Exception as e:
                print(f"Error notifying driver: {e}")
            
            await callback.message.edit_text(
                get_text("admin.verification_approved", "ru").format(user_id=driver_id)
            )
            await callback.answer("Верификация одобрена")
            
        elif action == "reject":
            # Отклоняем верификацию
            await UserRepository.update_verification(session, driver_id, False)
            
            # Отправляем уведомление водителю
            try:
                bot = callback.bot
                
                await bot.send_message(
                    chat_id=driver_id,
                    text=get_text("verification.rejected", driver_lang)
                )
            except Exception as e:
                print(f"Error notifying driver: {e}")
            
            await callback.message.edit_text(
                get_text("admin.verification_rejected", "ru").format(user_id=driver_id)
            )
            await callback.answer("Верификация отклонена")

