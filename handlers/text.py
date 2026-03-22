from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm.states import CreateGallery, RenameGallery
from database.connection import (
    register_user,
    add_new_gallery,
    get_galleries,
    delete_gallery,
    update_gallery_name,
)
from database.tables import check_gallery_exists
from keyboards.inline import get_galleries_list_kb, get_gallery_management_kb

router = Router()


@router.message(StateFilter("*"), Command("cancel"))
async def handle_cancel(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.clear()
    text = "Action canceled. ❌"
    if isinstance(event, types.Message):
        await event.answer(text)
    else:
        await event.message.edit_text(text)
        await event.answer()


@router.message(Command("start"))
async def handle_start(message: types.Message):
    register_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Welcome to the gallery bot, {message.from_user.first_name}!")


@router.message(Command("info"))
async def handle_info(message: types.Message):
    await message.answer(
        "This bot can save your images into galleries and show them to you whenever you want!"
    )


@router.message(Command("newgallery"))
async def handle_newgallery(message: types.Message, state: FSMContext):
    await message.answer("Please enter your gallery's name:")
    await state.set_state(CreateGallery.waiting_for_name)


@router.message(CreateGallery.waiting_for_name)
async def process_gallery_name(message: types.Message, state: FSMContext):
    if not message.text or message.text.startswith("/"):
        return await message.answer("Please send a valid name (not a command).")

    gallery_name = message.text.strip()
    tg_chat_id = message.from_user.id

    if len(gallery_name.split()) > 1:
        return await message.answer("Name should be one word. Try again or /cancel")

    if not (3 <= len(gallery_name) <= 30):
        return await message.answer(
            "Name must be 3-30 characters. Try again or /cancel"
        )

    if check_gallery_exists(tg_chat_id, gallery_name):
        return await message.answer(f"Gallery '{gallery_name}' already exists.")

    add_new_gallery(tg_chat_id, gallery_name)
    await message.answer(f"Gallery '{gallery_name}' created! ✅")
    await state.clear()


@router.message(Command("mygalleries"))
async def handle_mygalleries(message: types.Message):
    galleries = get_galleries(message.from_user.id)
    if not galleries:
        return await message.answer(
            "You don't have any galleries. Create one with /newgallery"
        )

    await message.answer(
        "Select a gallery to manage:", reply_markup=get_galleries_list_kb(galleries)
    )


@router.callback_query(F.data.startswith("select_"))
async def process_select_gallery(callback: types.CallbackQuery):
    gallery_name = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"Gallery: <b>{gallery_name}</b>\nWhat would you like to do?",
        reply_markup=get_gallery_management_kb(gallery_name),
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_list")
async def process_back_to_list(callback: types.CallbackQuery):
    galleries = get_galleries(callback.from_user.id)
    await callback.message.edit_text(
        "Select a gallery to manage:", reply_markup=get_galleries_list_kb(galleries)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("delete_"))
async def process_delete_gallery(callback: types.CallbackQuery):
    gallery_name = callback.data.split("_")[1]
    delete_gallery(callback.from_user.id, gallery_name)
    await callback.message.edit_text(f"Gallery '{gallery_name}' deleted! 🗑")
    await callback.answer()


@router.callback_query(F.data.startswith("rename_"))
async def process_rename_start(callback: types.CallbackQuery, state: FSMContext):
    gallery_name = callback.data.split("_")[1]
    await state.update_data(old_name=gallery_name)
    await callback.message.edit_text(f"Enter a new name for '{gallery_name}':")
    await state.set_state(RenameGallery.waiting_for_new_name)
    await callback.answer()


@router.message(RenameGallery.waiting_for_new_name)
async def process_rename_finish(message: types.Message, state: FSMContext):
    new_name = message.text.strip()
    data = await state.get_data()
    old_name = data.get("old_name")

    if len(new_name.split()) > 1 or not (3 <= len(new_name) <= 30):
        return await message.answer("Invalid name. Must be 3-30 characters, one word.")

    update_gallery_name(message.from_user.id, old_name, new_name)
    await message.answer(f"Renamed: {old_name} ➡️ {new_name} ✅")
    await state.clear()


@router.callback_query(F.data.startswith("view_"))
async def process_view_gallery(callback: types.CallbackQuery):
    gallery_name = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"Viewing photos in '{gallery_name}'... (Coming soon)"
    )
    await callback.answer()
