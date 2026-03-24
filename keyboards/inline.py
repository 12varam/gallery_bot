from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get_galleries_list_kb(galleries):
    builder = InlineKeyboardBuilder()
    for g in galleries:
        name = g[0]
        builder.row(
            types.InlineKeyboardButton(
                text=f"📁 {name}", callback_data=f"select_{name}"
            )
        )
    return builder.as_markup()


def get_gallery_management_kb(gallery_name):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text="🖼 View Images", callback_data=f"view_{gallery_name}")
    )
    builder.row(
        types.InlineKeyboardButton(
            text="➕ Add Photo", callback_data=f"addphoto_{gallery_name}"
        )
    ) 
    builder.row(
        types.InlineKeyboardButton(text="✏️ Rename", callback_data=f"rename_{gallery_name}")
    )
    builder.row(
        types.InlineKeyboardButton(text="🗑 Delete", callback_data=f"delete_{gallery_name}")
    )
    builder.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_list"))

    return builder.as_markup()
