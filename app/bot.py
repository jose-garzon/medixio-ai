from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from app.agent.agent import Agent
from app.modules.users.domain import UserMessenger

app = Dispatcher()


@app.message()
async def get_message(message: Message):
    if not message.from_user or not message.text:
        raise ValueError("There is no user")

    user = UserMessenger(
        messenger_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    question = message.text
    agent = Agent()
    response = await agent.ask(user, question)

    if response:
        await message.answer(response)


async def start_bot():
    token = getenv("BOT_TOKEN") or ""
    bot = Bot(token=token)
    await app.start_polling(bot)
