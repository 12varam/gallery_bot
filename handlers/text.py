from aiogram import Router, types
from aiogram.filters.command import Command
from database.connection import register_user


router = Router()


@router.message(Command("start"))
async def handle_start(message: types.Message):
    register_user(
        message.from_user.id,
        message.from_user.username
    )
    
    await message.answer(f"Welcome to the gallery bot {message.from_user.first_name}!")


@router.message(Command("info"))
async def handle_info(message: types.Message):
    await message.answer(
        "This bot can save your images into galleries and show them to you whenever you want!"
    )
