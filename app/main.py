import asyncio

from dotenv import load_dotenv

load_dotenv()
from .bot import start_bot


async def main():
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
