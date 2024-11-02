from aiogram import Bot, Dispatcher
from bot_token import Token
from Dispatchers.handlers import router
from Telegram.Database.models import database_main
import asyncio


async def main():
    bot = Bot(token=Token)
    dp = Dispatcher()
    dp.include_router(router)
    await database_main()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
