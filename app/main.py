import asyncio
import os

from aiogram import Bot, Dispatcher

import app.models  # noqa: F401 — ensures all models are registered before table creation
from app.db.session import create_db


async def main():
    bot = Bot(token=os.environ["BOT_TOKEN"])
    dispatcher = Dispatcher()

    await create_db()

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
