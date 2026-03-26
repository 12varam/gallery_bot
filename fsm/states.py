from aiogram.fsm.state import StatesGroup, State


class CreateGallery(StatesGroup):
    waiting_for_name = State()


class RenameGallery(StatesGroup):
    waiting_for_new_name = State()


class AddPhoto(StatesGroup):
    waiting_for_photo = State()
    waiting_for_description = State()


class RemovePhoto(StatesGroup):
    waiting_for_photo = State()
