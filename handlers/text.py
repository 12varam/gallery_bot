from aiogram import Router, types
from aiogram.filters.command import Command


router = Router()


@router.message(Command("start"))
async def handle_start(message: types.Message):
    await message.answer("Welcome to the gallery bot!")


@router.message(Command("info"))
async def handle_info(message: types.Message):
    await message.answer(
        "This bot can save your images into galleries and show them to you whenever you want!"
    )
