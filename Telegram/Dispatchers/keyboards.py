from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

about = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='About 💬', callback_data='About'),
                                               InlineKeyboardButton(text='Start ⭐️', callback_data='Start')]])

back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Back ✖️', callback_data='Back')]])


cancel_enter = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена ✖️',
                                                                           callback_data='Cancel_ent')]])
