from aiogram import Bot, Dispatcher
from bot_token import Token
from Dispatchers.handlers import router
import asyncio


async def main():
    bot = Bot(token=Token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
