from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Last expenses'),
            KeyboardButton('Categories')
        ],
        [
            KeyboardButton("Today's statistics"),
            KeyboardButton('Monthly statistics')
        ],
        [
            KeyboardButton('Help')
        ]
    ],
    resize_keyboard=True
)
