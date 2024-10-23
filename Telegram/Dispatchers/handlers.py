from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import Telegram.Dispatchers.keyboards as kb


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('👋 Привет! Я твой помощник-бот, который умеет парсить информацию с сайта telgra.ph!\n\n'
                         # ------------------
                         '🔍 Просто напиши, что именно тебя интересует, и я быстро найду нужные данные для тебя.\n\n'
                         # ------------------
                         '💳 Стоимость подписки: [вставь сумму] в месяц. Подписка дает доступ ко всем функциям и '
                         'обновлениям!\n\n'
                         # ------------------
                         '💎 У нас есть пробный период на 7 дней, чтобы ты мог оценить все возможности сервиса без '
                         'обязательств!\n\n', reply_markup=kb.about)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Привет! 👋 Я твой помощник-бот, который поможет тебе'
                         'парсить информацию с сайта telgra.ph. Просто дай мне'
                         'команду, и я найду нужные данные для тебя! Чем могу помочь'
                         'сегодня? 🚀')


@router.callback_query(F.data == 'About')
async def about(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Привет! 👋 Я твой помощник-бот, который поможет тебе'
                                     'парсить информацию с сайта telgra.ph. Просто дай мне'
                                     'команду, и я найду нужные данные для тебя! Чем могу помочь'
                                     'сегодня? 🚀', reply_markup=kb.back)


@router.callback_query(F.data == 'Back')
async def about(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('👋 Привет! Я твой помощник-бот, который умеет парсить'
                                     ' информацию с сайта telgra.ph!\n\n'
                                     # ------------------
                                     '🔍 Просто напиши, что именно тебя интересует,'
                                     ' и я быстро найду нужные данные для тебя.\n\n'
                                     # ------------------
                                     '💳 Стоимость подписки: [вставь сумму] в месяц. Подписка дает'
                                     ' доступ ко всем функциям и '
                                     'обновлениям!\n\n'
                                     # ------------------
                                     '💎 У нас есть пробный период на 7 дней, чтобы'
                                     ' ты мог оценить все возможности сервиса без '
                                     'обязательств!\n\n', reply_markup=kb.about)
