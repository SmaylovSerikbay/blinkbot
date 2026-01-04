"""
Состояния FSM для водителя
"""
from aiogram.fsm.state import State, StatesGroup


class CreateTripStates(StatesGroup):
    """Состояния создания поездки"""
    from_city = State()
    to_city = State()
    trip_date = State()
    price = State()
    description = State()

