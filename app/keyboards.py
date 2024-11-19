from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

keyboard_days = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Сьогодні', callback_data='day-1'),
        InlineKeyboardButton(text='Тиждень', callback_data='day-7'),
        InlineKeyboardButton(text='10 днів', callback_data='day-10')
    ]
])

keyboard_citys = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Суми'),
        KeyboardButton(text='Київ'),
        KeyboardButton(text='Харків')
    ],
    [
        KeyboardButton(text='Одеса'),
        KeyboardButton(text='Львів'),
        KeyboardButton(text='Дніпро')
    ]
], resize_keyboard=True, one_time_keyboard=True)
