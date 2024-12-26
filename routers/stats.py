from aiogram.fsm.state import State, StatesGroup


class SaveUser(StatesGroup):
    name = State()
    level = State()


class PollHandler(StatesGroup):
    cur_question_index = State()
    correct_answers = State()
    correct_option_id = State()
    chat_id = State()
    message = State()
