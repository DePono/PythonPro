from aiogram.fsm.state import State, StatesGroup

class AddTaskState(StatesGroup):
    waiting_for_name = State()
    waiting_for_deadline = State()
