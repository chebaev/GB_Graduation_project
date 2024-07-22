from aiogram.fsm.state import StatesGroup, State


class StateDate(StatesGroup):
    start_date = State()
    end_date = State()

class StateUser(StatesGroup):
    user_telegram_id = State()
    user_days = State()

class StateVerification(StatesGroup):
    user_telegram_id = State()


class AdminPanel(StatesGroup):
    user_message = State()

class AdminPanel_BD(StatesGroup):
    name = State()
    receive_message = State()
