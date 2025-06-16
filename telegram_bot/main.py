import asyncio, aiohttp, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fsm import AddTaskState
from keyboards import delete_keyboard
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def cmd_start(msg: types.Message):
    await msg.answer("Привет! Команды: /add_task /show_tasks /delete_task")

@dp.message(F.text == "/add_task")
async def add_task_start(msg: types.Message, state: FSMContext):
    await state.set_state(AddTaskState.waiting_for_name)
    await msg.answer("Введите название задачи:")

@dp.message(AddTaskState.waiting_for_name)
async def task_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(AddTaskState.waiting_for_deadline)
    await msg.answer("Введите дедлайн (ДД.ММ.ГГГГ):")

@dp.message(AddTaskState.waiting_for_deadline)
async def task_deadline(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    async with aiohttp.ClientSession() as session:
        resp = await session.post(f"{API_URL}/tasks", json={
            "name": data["name"],
            "deadline": msg.text
        })
        if resp.status == 200:
            await msg.answer("Задача добавлена!")
        else:
            await msg.answer("Ошибка добавления.")
    await state.clear()

@dp.message(F.text == "/show_tasks")
async def show_tasks(msg: types.Message):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(f"{API_URL}/tasks")
        if resp.status != 200:
            await msg.answer("Ошибка загрузки задач.")
            return
        tasks = await resp.json()
        if not tasks:
            await msg.answer("Задач нет.")
        else:
            text = "\n".join([f"{t['id']}. {t['name']} (дедлайн: {t['deadline']})" for t in tasks])
            await msg.answer(text)

@dp.message(F.text == "/delete_task")
async def delete_task(msg: types.Message):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(f"{API_URL}/tasks")
        tasks = await resp.json()
        if not tasks:
            await msg.answer("Задач нет.")
        else:
            await msg.answer("Выберите задачу:", reply_markup=delete_keyboard(tasks))

@dp.callback_query(F.data.startswith("delete:"))
async def handle_delete(call: types.CallbackQuery):
    task_id = call.data.split(":")[1]
    async with aiohttp.ClientSession() as session:
        resp = await session.delete(f"{API_URL}/tasks/{task_id}")
        if resp.status == 200:
            await call.message.answer(f"Задача {task_id} удалена.")
        else:
            await call.message.answer("Ошибка удаления.")
    await call.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
