from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm.states import CreateGallery, RenameGallery, AddPhoto
from database.connection import (
    register_user,
    add_new_gallery,
    get_galleries,
    delete_gallery,
    update_gallery_name,
    add_image_to_db,
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
    if not message.text:
        return await message.answer(
            "Please send a <b>text</b> name for the gallery. Stickers or photos are not allowed! ❌"
        )

    if message.text.startswith("/"):
        return await message.answer(
            "Gallery name cannot start with '/'. Please enter a plain word or /cancel."
        )

    new_name = message.text.strip()
    data = await state.get_data()
    old_name = data.get("old_name")
    tg_chat_id = message.from_user.id

    if len(new_name.split()) > 1 or not (3 <= len(new_name) <= 30):
        return await message.answer(
            "Invalid name. Use one word (3-30 characters). Try again or /cancel"
        )

    if check_gallery_exists(tg_chat_id, new_name):
        return await message.answer(
            f"Gallery with name '{new_name}' already exists! Choose another name."
        )

    update_gallery_name(tg_chat_id, old_name, new_name)
    await message.answer(
        f"Success! Gallery renamed: <b>{old_name}</b> ➡️ <b>{new_name}</b> ✅"
    )
    await state.clear()


@router.callback_query(F.data.startswith("view_"))
async def process_view_gallery(callback: types.CallbackQuery):
    gallery_name = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"Viewing photos in '{gallery_name}'... (Coming soon)"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("addphoto_"))
async def process_add_photo_start(callback: types.CallbackQuery, state: FSMContext):
    gallery_name = callback.data.split("_")[1]

    await state.update_data(selected_gallery=gallery_name)

    await callback.message.edit_text(
        f"Selected gallery: <b>{gallery_name}</b>\n\nPlease send me the photo you want to add. 📸"
    )
    await state.set_state(AddPhoto.waiting_for_photo)
    await callback.answer()


@router.message(AddPhoto.waiting_for_photo, F.photo)
async def process_photo_received(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)

    data = await state.get_data()
    gallery_name = data.get("selected_gallery")

    await message.answer(
        f"Got it! Now send a description for this photo to save it in <b>{gallery_name}</b> (or /skip):"
    )
    await state.set_state(AddPhoto.waiting_for_description)


@router.message(AddPhoto.waiting_for_description)
async def process_photo_description_final(message: types.Message, state: FSMContext):
    if not message.text and not message.caption:
        return await message.answer("Please send description as text or /skip")

    text = message.text or message.caption
    description = "" if text == "/skip" else text

    data = await state.get_data()
    photo_id = data.get("photo_id")
    gallery_name = data.get("selected_gallery")

    add_image_to_db(message.from_user.id, photo_id, gallery_name, description)
    await message.answer(f"Photo successfully saved to <b>{gallery_name}</b>! ✅")
    await state.clear()
