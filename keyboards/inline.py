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
        types.InlineKeyboardButton(
            text="🖼 View Images", callback_data=f"view_{gallery_name}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="➕ Add Photo", callback_data=f"addphoto_{gallery_name}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="✏️ Rename", callback_data=f"rename_{gallery_name}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🗑 Delete", callback_data=f"deletegallery_{gallery_name}"
        )
    )
    builder.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_list"))

    return builder.as_markup()


def get_confirm_delete_kb(gallery_name):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="✅ Yes, delete", callback_data=f"confirm_del_{gallery_name}"
        ),
        types.InlineKeyboardButton(text="❌ cancel", callback_data=f"cancel_delete"),
    )

    return builder.as_markup()


def get_photo_actions_kb(photo_id):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="📝 Edit Desc", callback_data=f"editdesc_{photo_id}"
        ),
        types.InlineKeyboardButton(
            text="🔄 Change Photo", callback_data=f"editfile_{photo_id}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🗑 Delete Photo", callback_data=f"delete_photo_{photo_id}"
        )
    )

    return builder.as_markup()


def get_photos_pagination_list_kb(images, gallery_name, page=1):
    builder = InlineKeyboardBuilder()

    start_index = (page - 1) * 10
    end_index = start_index + 10

    current_page_images = images[start_index:end_index]

    for photo_id, _, desc in current_page_images:
        short_desc = (desc[:20] + "...") if desc else f"ID: {photo_id}"
        builder.row(
            types.InlineKeyboardButton(
                text=f"🖼 {short_desc}", callback_data=f"showphoto_{photo_id}"
            )
        )

    nav_buttons = []
    total_pages = (len(images) + 9) // 10

    nav_buttons.append(
        types.InlineKeyboardButton(
            text="⬅️ Prev", callback_data=f"listpage_{gallery_name}_{page - 1}"
        )
    )

    nav_buttons.append(
        types.InlineKeyboardButton(
            text=f"{page} / {total_pages}", callback_data="ignore"
        )
    )

    nav_buttons.append(
        types.InlineKeyboardButton(
            text="Next ➡️", callback_data=f"listpage_{gallery_name}_{page + 1}"
        )
    )

    builder.row(*nav_buttons)
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️ Back to Menu", callback_data=f"select_{gallery_name}"
        )
    )

    return builder.as_markup()
