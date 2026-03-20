from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


class CreateGallery(StatesGroup):
    waiting_for_name = State()
