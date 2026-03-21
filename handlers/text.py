from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm.states import CreateGallery, DeleteGallery
from database.connection import (
    register_user,
    add_new_gallery,
    get_galleries,
    delete_gallery,
)
from database.tables import check_gallery_exists


router = Router()


@router.message(StateFilter("*"), Command("cancel"))
async def handle_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("canceled ❌")


@router.message(Command("deletegallery"))
async def handle_deletegallery(message: types.Message, state: FSMContext):
    galleries = get_galleries(message.from_user.id)

    if not galleries:
        return await message.answer("You don't have any galleries to delete")

    names = ", ".join([g[0] for g in galleries])
    await message.answer(
        f"Your galleries: {names}\nWrite the name of the gallery that you wanna delete:"
    )
    await state.set_state(DeleteGallery.waiting_for_name)


@router.message(DeleteGallery.waiting_for_name)
async def process_deletegallery(message: types.Message, state: FSMContext):
    gallery_name = message.text.strip()
    tg_chat_id = message.from_user.id

    if not check_gallery_exists(tg_chat_id, gallery_name):
        return await message.answer(
            "There's no such a gallery. Let's try again or write /cancel"
        )

    delete_gallery(tg_chat_id, gallery_name)

    await message.answer(f"Gallery {gallery_name} has successfully been deleted!")
    await state.clear()


@router.message(Command("start"))
async def handle_start(message: types.Message):
    register_user(message.from_user.id, message.from_user.username)

    await message.answer(f"Welcome to the gallery bot {message.from_user.first_name}!")


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
    if not message.text:
        return await message.answer("Gallery's name should be text, nothing else!")

    gallery_name = message.text.strip()
    tg_chat_id = message.from_user.id

    if len(gallery_name.split()) > 1:
        return await message.answer(
            "Gallery's name should be made of 1 word. Let's try something else or write /cancel"
        )

    if len(gallery_name) < 3 or len(gallery_name) > 30:
        return await message.answer(
            "Gallery's name shouldn't be shorter than 3 and longer than 30 symbols. Let's try something else or write /cancel"
        )

    if check_gallery_exists(tg_chat_id, gallery_name):
        return await message.answer(
            f"Gallery named '{gallery_name}' already exists. Let's try something else or write /cancel"
        )

    add_new_gallery(tg_chat_id, gallery_name)
    await message.answer(f"Gallery '{gallery_name}' was successfully created!")

    await state.clear()


@router.message(Command("mygalleries"))
async def handle_mygalleries(message: types.Message):
    galleries = get_galleries(message.from_user.id)

    galleries_corrected = []

    for g in galleries:
        galleries_corrected.append(g[0])

    galleries_formatted = ""

    for g_name in galleries_corrected:
        galleries_formatted += f"{g_name}\n"

    await message.answer(
        f"""
        here's the list of your galleries:
{galleries_formatted}
    """
    )
