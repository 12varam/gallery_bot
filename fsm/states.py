from aiogram.fsm.state import StatesGroup, State


class CreateGallery(StatesGroup):
    waiting_for_name = State()


class DeleteGallery(StatesGroup):
    waiting_for_name = State()
