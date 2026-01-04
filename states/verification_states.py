"""
Состояния FSM для верификации водителя
"""
from aiogram.fsm.state import State, StatesGroup


class VerificationStates(StatesGroup):
    """Состояния верификации"""
    license_photo = State()  # Фото прав
    car_photo = State()  # Фото машины

