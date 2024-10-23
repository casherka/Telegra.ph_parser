from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

about = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='About 💬', callback_data='About')]])

back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Back ✖️', callback_data='Back')]])
