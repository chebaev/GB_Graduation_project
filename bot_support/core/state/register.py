from aiogram.fsm.state import StatesGroup, State


class RegAnswer(StatesGroup):
    telegram_id = State()
    question = State()
    answer = State()
    activity = State()
