from aiogram.dispatcher.filters.state import State, StatesGroup


class Survey(StatesGroup):
    waiting_day = State()
    waiting_humans = State()
    waiting_address = State()
    waiting_time = State()
    waiting_task = State()
    waiting_pay = State()
    waiting_confirm = State()
    waiting_payment_confirm = State()

class SurveyForAdmin(StatesGroup):
    waiting_edit = State()