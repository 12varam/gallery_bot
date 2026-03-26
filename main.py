import logging
from config.loader import settings
from handlers.text import router as main_router
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode="HTML"))

    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="info", description="Get information about this bot"),
            BotCommand(command="newgallery", description="Create a new gallery"),
            BotCommand(command="mygalleries", description="Manage your galleries"),
            BotCommand(command="cancel", description="Cancel the current operation"),
        ]
    )

    dp = Dispatcher()
    dp.include_router(main_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
