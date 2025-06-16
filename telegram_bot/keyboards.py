from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def delete_keyboard(tasks):
    buttons = [
        [InlineKeyboardButton(text=f"Удалить {t['id']}", callback_data=f"delete:{t['id']}")]
        for t in tasks
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
