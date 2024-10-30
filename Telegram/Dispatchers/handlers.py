from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import Telegram.Dispatchers.keyboards as kb
import multiprocessing
import os
from parser import bot_main


router = Router()


class InputTitle(StatesGroup):
    Title = State()


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


@router.callback_query(F.data == 'About')
async def about(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Привет! 👋 Я твой помощник-бот, который поможет тебе '
                                     'парсить информацию с сайта telgra.ph. Просто дай мне '
                                     'команду, и я найду нужные данные для тебя! Чем могу помочь '
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


@router.callback_query(F.data == 'Start')
async def input_title(callback: CallbackQuery, state: FSMContext):
    await state.set_state(InputTitle.Title)
    await callback.message.edit_text('Введите название:', reply_markup=kb.cancel_enter)
    await callback.answer('')


@router.message(InputTitle.Title)
async def start(message: Message, state: FSMContext):
    await state.update_data(Title=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(f"Запуск с названием: {data['Title']}...")
    try:
        os.mkdir(str(message.from_user.id))
    except FileExistsError:
        pass

    process = multiprocessing.Process(target=bot_main, args=(data['Title'], message.from_user.id,))
    process.start()


@router.callback_query(F.data == 'Cancel_ent')
async def input_title(callback: CallbackQuery, state: FSMContext):
    state_chk = await state.get_state()
    if state_chk == 'InputTitle:Title':
        await state.clear()
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
    else:
        await callback.message.delete()
    await callback.answer('')
