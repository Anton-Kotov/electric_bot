import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from environs import Env
from handlers.menu import register_menu


def register_all_handlers(dp):
    register_menu(dp)

async def main():
    env = Env()
    env.read_env()
    BOT_TOKEN = env.str("TOKEN")
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_all_handlers(dp)

    try:
        await dp.start_polling()

    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await dp.stop_polling()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass