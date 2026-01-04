"""
Inline клавиатуры
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from locales.translations import SUPPORTED_LANGUAGES


def get_language_keyboard() -> InlineKeyboardBuilder:
    """Клавиатура для выбора языка"""
    builder = InlineKeyboardBuilder()
    
    languages = {
        "kz": "🇰🇿 Қазақша",
        "ru": "🇷🇺 Русский",
        "uz": "🇺🇿 O'zbekcha",
        "en": "🇬🇧 English",
    }
    
    for lang_code in SUPPORTED_LANGUAGES:
        builder.button(text=languages[lang_code], callback_data=f"lang_{lang_code}")
    
    builder.adjust(2)  # По 2 кнопки в ряду
    return builder.as_markup()


def get_role_keyboard(lang: str = "ru") -> InlineKeyboardBuilder:
    """Клавиатура для выбора роли"""
    from locales.translations import get_text
    
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=get_text("start.driver", lang),
        callback_data="role_driver"
    )
    builder.button(
        text=get_text("start.passenger", lang),
        callback_data="role_passenger"
    )
    
    builder.adjust(1)  # По 1 кнопке в ряду
    return builder.as_markup()


def get_trip_navigation_keyboard(lang: str = "ru", trip_id: int = None) -> InlineKeyboardBuilder:
    """Клавиатура для навигации по карточкам поездок"""
    from locales.translations import get_text
    
    builder = InlineKeyboardBuilder()
    
    if trip_id:
        builder.button(
            text=get_text("common.contact", lang),
            callback_data=f"contact_{trip_id}"
        )
    
    builder.button(
        text=get_text("common.next", lang),
        callback_data="next_trip"
    )
    
    builder.adjust(2)
    return builder.as_markup()


def get_phone_request_keyboard(lang: str = "ru") -> InlineKeyboardBuilder:
    """Клавиатура для запроса телефона"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    from locales.translations import get_text
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("common.share_phone", lang), request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_admin_verification_keyboard(user_id: int) -> InlineKeyboardBuilder:
    """Клавиатура для администратора (одобрить/отклонить верификацию)"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="✅ Одобрить", callback_data=f"admin_verify_approve_{user_id}")
    builder.button(text="❌ Отклонить", callback_data=f"admin_verify_reject_{user_id}")
    
    builder.adjust(2)
    return builder.as_markup()

