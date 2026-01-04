"""
Утилиты для форматирования карточек поездок
"""
from datetime import datetime
from typing import Optional
from locales.translations import get_text


def format_trip_card(trip, driver, lang: str = "ru") -> str:
    """
    Форматирует карточку поездки с информацией о водителе, рейтинге и верификации
    
    Args:
        trip: Объект Trip из БД
        driver: Объект User (водитель) из БД
        lang: Язык для локализации
    
    Returns:
        Отформатированная строка с информацией о поездке
    """
    # Форматируем дату
    trip_date_str = trip.trip_date.strftime("%d.%m.%Y %H:%M") if isinstance(trip.trip_date, datetime) else str(trip.trip_date)
    
    # Формируем имя водителя
    driver_name = driver.first_name or "Не указано"
    if driver.last_name:
        driver_name += f" {driver.last_name}"
    
    # Значок верификации
    verified_icon = "✅" if driver.is_verified else ""
    
    # Форматируем рейтинг (звезды)
    rating_stars = "⭐" * int(driver.rating) + ("⭐" if driver.rating - int(driver.rating) >= 0.5 else "")
    rating_text = f"{rating_stars} {driver.rating:.1f}"
    
    # Информация об автомобиле
    car_info = get_text("passenger.car_model", lang)
    if driver.car_photo_id:
        car_info = "📷 Фото прикреплено"  # Можно добавить локализацию
    
    # Описание поездки
    description = ""
    if trip.description:
        description = f"\n📝 {trip.description}"
    
    # Формируем карточку
    card_text = get_text("passenger.trip_card", lang).format(
        from_city=trip.from_city,
        to_city=trip.to_city,
        date=trip_date_str,
        price=trip.price,
        name=driver_name,
        verified=verified_icon,
        rating=rating_text,
        car_info=car_info,
        username=driver.username or "",
        description=description
    )
    
    return card_text

