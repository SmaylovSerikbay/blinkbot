"""
Централизованная система переводов
"""
from . import ru, kz, uz, en

# Поддерживаемые языки
SUPPORTED_LANGUAGES = ["ru", "kz", "uz", "en"]
DEFAULT_LANGUAGE = "ru"

# Словарь всех переводов
TRANSLATIONS = {
    "ru": ru.translations,
    "kz": kz.translations,
    "uz": uz.translations,
    "en": en.translations,
}


def get_text(key: str, lang: str = DEFAULT_LANGUAGE) -> str:
    """
    Получить переведенный текст по ключу
    
    Args:
        key: Ключ перевода (например, "start.welcome")
        lang: Код языка (ru, kz, uz, en)
    
    Returns:
        Переведенный текст или ключ, если перевод не найден
    """
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    
    translations = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE])
    
    # Поддержка вложенных ключей через точку (например, "start.welcome")
    keys = key.split(".")
    result = translations
    
    try:
        for k in keys:
            result = result[k]
        return result if isinstance(result, str) else key
    except (KeyError, TypeError):
        # Если перевод не найден, пытаемся получить из дефолтного языка
        if lang != DEFAULT_LANGUAGE:
            return get_text(key, DEFAULT_LANGUAGE)
        return key

