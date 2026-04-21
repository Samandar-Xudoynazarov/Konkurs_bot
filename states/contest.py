from aiogram.fsm.state import State, StatesGroup


class CreateContest(StatesGroup):
    title = State()
    description = State()
    prizes = State()
    winners_count = State()
    max_participants = State()
    start_date = State()
    end_date = State()
    channels = State()
