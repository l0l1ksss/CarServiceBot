from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_name = State()


class RegistrationCarStates(StatesGroup):
    waiting_for_plate = State()
    waiting_for_vin = State()
    waiting_for_brand = State()
    waiting_for_model = State()
    waiting_for_year = State()
    waiting_for_config = State()
    waiting_for_dealer = State()
    waiting_for_color = State()

class PutHistoryStates(StatesGroup):
    waiting_for_official = State()
    waiting_for_type = State()
    waiting_for_comment = State()
    waiting_for_mileage = State()