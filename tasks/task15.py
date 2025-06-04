import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"

# Простое хранилище заметок на время работы бота
user_notes = {}

# Определение машины состояний
class NoteStates(StatesGroup):
    Start = State()
    AddNote = State()
    DeleteNote = State()

#Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню (инлайн-клавиатура)
def get_main_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Добавить заметку", callback_data="add")
    kb.button(text="Просмотреть заметки", callback_data="view")
    kb.button(text="Удалить заметку", callback_data="delete")
    return kb.as_markup()

#Динамическая клавиатура удаления
def get_delete_keyboard(notes: list[str]):
    kb = InlineKeyboardBuilder()
    for idx, note in enumerate(notes):
        kb.button(text=note, callback_data=f"del_{idx}")
    return kb.as_markup()

#Старт-команда
@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(NoteStates.Start)
    await message.answer("Привет! Что вы хотите сделать?", reply_markup=get_main_keyboard())

#бработка выбора из главного меню
@dp.callback_query(F.data.in_(["add", "view", "delete"]))
async def handle_menu(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    notes = user_notes.get(user_id, [])

    if callback.data == "add":
        await state.set_state(NoteStates.AddNote)
        await callback.message.answer("Введите текст новой заметки:")
    elif callback.data == "view":
        if notes:
            text = "\n".join(f"{i+1}. {n}" for i, n in enumerate(notes))
        else:
            text = "У вас пока нет заметок."
        await callback.message.answer(text)
    elif callback.data == "delete":
        if notes:
            await state.set_state(NoteStates.DeleteNote)
            await callback.message.answer("Выберите заметку для удаления:", reply_markup=get_delete_keyboard(notes))
        else:
            await callback.message.answer("У вас пока нет заметок.")

    await callback.answer()

# Приём текста заметки
@dp.message(NoteStates.AddNote)
async def add_note(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_notes.setdefault(user_id, []).append(message.text)
    await message.answer("Заметка добавлена!", reply_markup=get_main_keyboard())
    await state.set_state(NoteStates.Start)

#Обработка удаления
@dp.callback_query(F.data.startswith("del_"))
async def delete_note(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    index = int(callback.data.split("_")[1])
    try:
        removed = user_notes[user_id].pop(index)
        await callback.message.answer(f"Удалена заметка: {removed}", reply_markup=get_main_keyboard())
    except IndexError:
        await callback.message.answer("Неверный индекс.")
    await state.set_state(NoteStates.Start)
    await callback.answer()

#Запуск
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
