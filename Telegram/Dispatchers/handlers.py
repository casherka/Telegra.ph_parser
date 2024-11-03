from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import Telegram.Dispatchers.keyboards as kb
import multiprocessing
import os
from parser import bot_main
import Telegram.Database.requests as db


router = Router()


class InputTitle(StatesGroup):
    Input = State()


class GivePremiumInput(StatesGroup):
    Input = State()


class ClaimPremiumInput(StatesGroup):
    Input = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await db.set_user(message.from_user.id, message.from_user.username,
                      f"{message.from_user.first_name} {message.from_user.last_name}")
    premium = await db.get_premium(message.from_user.id)
    admin = await db.get_admin(message.from_user.id)
    if admin and premium:
        await message.answer('👋 Привет! Я твой помощник-бот, который умеет парсить информацию с сайта telgra.ph!\n\n'
                             # ------------------
                             '💎 Премиум активирован.\n\n'
                             # ------------------
                             '👑 Админ режим.', reply_markup=kb.about_admin)
    elif admin and not premium:
        await message.answer('👋 Привет! Я твой помощник-бот, который умеет парсить информацию с сайта telgra.ph!\n\n'
                             # ------------------
                             '💎 Премиум не активирован.\n\n'
                             # ------------------
                             '👑 Админ режим.', reply_markup=kb.about_admin)
    elif premium and not admin:
        await message.answer('👋 Привет! Я твой помощник-бот, который умеет парсить информацию с сайта telgra.ph!\n\n'
                             # ------------------
                             '🔍 Просто напиши, что именно тебя интересует, и я быстро найду нужные данные для тебя.\n\n'
                             # ------------------
                             '💎 Премиум активирован.', reply_markup=kb.about)
    elif not premium and not admin:
        await message.answer('👋 Привет! Я твой помощник-бот, который умеет парсить информацию с сайта telgra.ph!\n\n'
                             # ------------------
                             '🔍 Просто напиши, что именно тебя интересует, и я быстро найду нужные данные для тебя.\n\n'
                             # ------------------
                             '💳 Стоимость подписки: [вставь сумму] в месяц. Подписка дает доступ ко всем функциям и '
                             'обновлениям!\n\n'
                             # ------------------
                             '💎 У нас есть пробный период на 6 дней, чтобы ты мог оценить все возможности сервиса без '
                             'обязательств!', reply_markup=kb.about)


@router.callback_query(F.data == 'About')
async def about(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Привет! 👋 Я твой помощник-бот, который поможет тебе '
                                     'парсить информацию с сайта telgra.ph. Просто дай мне '
                                     'команду, и я найду нужные данные для тебя! Чем могу помочь '
                                     'сегодня? 🚀', reply_markup=kb.back)


@router.callback_query(F.data == 'Back')
async def about_back(callback: CallbackQuery):
    await callback.answer('')
    premium = await db.get_premium(callback.from_user.id)
    admin = await db.get_admin(callback.from_user.id)
    if admin and premium:
        await callback.message.edit_text('👋 Привет! Я твой помощник-бот,'
                                         ' который умеет парсить информацию с сайта telgra.ph!\n\n'
                                         # ------------------
                                         '💎 Премиум активирован.\n\n'
                                         # ------------------
                                         '👑 Админ режим.', reply_markup=kb.about_admin)
    elif admin and not premium:
        await callback.message.edit_text('👋 Привет! Я твой помощник-бот, который '
                                         'умеет парсить информацию с сайта telgra.ph!\n\n'
                                         # ------------------
                                         '💎 Премиум не активирован.\n\n'
                                         # ------------------
                                         '👑 Админ режим.', reply_markup=kb.about_admin)
    elif premium and not admin:
        await callback.message.edit_text('👋 Привет! Я твой помощник-бот, который '
                                         'умеет парсить информацию с сайта telgra.ph!\n\n'
                                         # ------------------
                                         '🔍 Просто напиши, что именно тебя интересует, '
                                         'и я быстро найду нужные данные для тебя.\n\n'
                                         # ------------------
                                         '💎 Премиум активирован.', reply_markup=kb.about)
    elif not premium and not admin:
        await callback.message.edit_text('👋 Привет! Я твой помощник-бот, который умеет'
                                         ' парсить информацию с сайта telgra.ph!\n\n'
                                         # ------------------
                                         '🔍 Просто напиши, что именно тебя интересует,'
                                         ' и я быстро найду нужные данные для тебя.\n\n'
                                         # ------------------
                                         '💳 Стоимость подписки: [вставь сумму] в месяц.'
                                         ' Подписка дает доступ ко всем функциям и '
                                         'обновлениям!\n\n'
                                         # ------------------
                                         '💎 У нас есть пробный период на 6 дней,'
                                         ' чтобы ты мог оценить все возможности сервиса без '
                                         'обязательств!', reply_markup=kb.about)


@router.callback_query(F.data == 'Start')
async def input_title(callback: CallbackQuery, state: FSMContext):
    await state.set_state(InputTitle.Input)
    await callback.message.edit_text('Введите название:', reply_markup=kb.cancel_enter)
    await callback.answer('')


@router.callback_query(F.data == 'Give_premium')
async def input_give_id(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GivePremiumInput.Input)
    await callback.message.edit_text('Введите Id:', reply_markup=kb.cancel_enter)
    await callback.answer('')


@router.callback_query(F.data == 'Claim_premium')
async def input_claim_id(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ClaimPremiumInput.Input)
    await callback.message.edit_text('Введите Id:', reply_markup=kb.cancel_enter)
    await callback.answer('')


@router.message(ClaimPremiumInput.Input)
async def claim_premium(message: Message, state: FSMContext):
    await state.update_data(Id=message.text)
    data = await state.get_data()
    await state.clear()
    admin = await db.get_admin(message.from_user.id)
    if admin:
        await db.delete_premium(data['Id'])
        await message.answer(f"🗑 Премиум удалён у {data['Id']}")
    else:
        await message.answer(f"🚫 Отказано в доступе")


@router.message(GivePremiumInput.Input)
async def give_premium(message: Message, state: FSMContext):
    await state.update_data(Id=message.text)
    data = await state.get_data()
    await state.clear()
    admin = await db.get_admin(message.from_user.id)
    if admin:
        await db.set_premium(data['Id'])
        await message.answer(f"🎁 Премиум выдан {data['Id']}")
    else:
        await message.answer(f"🚫 Отказано в доступе")


@router.message(InputTitle.Input)
async def start(message: Message, state: FSMContext):
    await state.update_data(Title=message.text)
    data = await state.get_data()
    await state.clear()
    premium = await db.get_premium(message.from_user.id)
    if premium:
        await message.answer(f"⏳ Запуск с названием: {data['Title']}...")
        try:
            os.mkdir(str(message.from_user.id))
        except FileExistsError:
            pass

        process = multiprocessing.Process(target=bot_main, args=(data['Title'], message.from_user.id,))
        process.start()
    else:
        await message.answer(f'''⚠️ Запуск "{data['Title']}" отменён\n\n'''
                             f"🔑 Премиум не активирован")


@router.callback_query(F.data == 'Cancel_ent')
async def cancel_input(callback: CallbackQuery, state: FSMContext):
    state_chk = await state.get_state()
    if state_chk == 'InputTitle:Input' or 'GivePremiumInput:Input' or 'ClaimPremiumInput:Input':
        await state.clear()
        premium = await db.get_premium(callback.from_user.id)
        admin = await db.get_admin(callback.from_user.id)
        if admin and premium:
            await callback.message.edit_text('👋 Привет! Я твой помощник-бот,'
                                             ' который умеет парсить информацию с сайта telgra.ph!\n\n'
                                             # ------------------
                                             '💎 Премиум активирован.\n\n'
                                             # ------------------
                                             '👑 Админ режим.', reply_markup=kb.about_admin)
        elif admin and not premium:
            await callback.message.edit_text('👋 Привет! Я твой помощник-бот, который '
                                             'умеет парсить информацию с сайта telgra.ph!\n\n'
                                             # ------------------
                                             '💎 Премиум не активирован.\n\n'
                                             # ------------------
                                             '👑 Админ режим.', reply_markup=kb.about_admin)
        elif premium and not admin:
            await callback.message.edit_text('👋 Привет! Я твой помощник-бот, который '
                                             'умеет парсить информацию с сайта telgra.ph!\n\n'
                                             # ------------------
                                             '🔍 Просто напиши, что именно тебя интересует, '
                                             'и я быстро найду нужные данные для тебя.\n\n'
                                             # ------------------
                                             '💎 Премиум активирован.', reply_markup=kb.about)
        elif not premium and not admin:
            await callback.message.edit_text('👋 Привет! Я твой помощник-бот, который умеет'
                                             ' парсить информацию с сайта telgra.ph!\n\n'
                                             # ------------------
                                             '🔍 Просто напиши, что именно тебя интересует,'
                                             ' и я быстро найду нужные данные для тебя.\n\n'
                                             # ------------------
                                             '💳 Стоимость подписки: [вставь сумму] в месяц.'
                                             ' Подписка дает доступ ко всем функциям и '
                                             'обновлениям!\n\n'
                                             # ------------------
                                             '💎 У нас есть пробный период на 6 дней,'
                                             ' чтобы ты мог оценить все возможности сервиса без '
                                             'обязательств!', reply_markup=kb.about)
    else:
        await callback.message.delete()
    await callback.answer('')
