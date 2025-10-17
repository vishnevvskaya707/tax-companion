from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_periods_keyboard():
    periods = ['янв.', 'февр.', 'мар.', 'апр.', 'май', 'июн.', 'июл.', 'авг.','сент.', 'окт.', 'нояб.', 'дек.']
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{period} 2025', callback_data=f'period_{period} 2025')
         for period in periods[i:i+4]]
         for i in range(0, 12, 4)
    ])