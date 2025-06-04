from aiogram import Bot, Dispatcher, types, F
from aiogram.types import LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters import Command
import sqlite3
import asyncio
from datetime import datetime

BOT_TOKEN = ""
PAYMENT_TOKEN = ""  # Тестовый токен Telegram
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 💾 SQLite: создаем таблицу для платежей
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    product_name TEXT,
    amount INTEGER,
    currency TEXT,
    status TEXT,
    timestamp TEXT
)
''')
conn.commit()

# 🛍️ Список товаров
products = {
    "notebook": {
        "title": "Записная книжка",
        "description": "Классическая бумажная записная книжка",
        "price": 199
    },
    "pen": {
        "title": "Ручка",
        "description": "Шариковая ручка с логотипом",
        "price": 99
    }
}

# 🛒 Магазин
@dp.message(Command("shop"))
async def shop(message: types.Message):
    kb = InlineKeyboardBuilder()
    for key, product in products.items():
        kb.button(text=product["title"], callback_data=f"buy_{key}")
    await message.answer("Выберите товар:", reply_markup=kb.as_markup())

# 💸 Выставляем счёт
@dp.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: types.CallbackQuery):
    product_key = callback.data.replace("buy_", "")
    product = products[product_key]

    prices = [LabeledPrice(label=product["title"], amount=product["price"] * 100)]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=product["title"],
        description=product["description"],
        payload=product_key,
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="test-bot"
    )
    await callback.answer()

# ✅ Подтверждение оплаты
@dp.pre_checkout_query()
async def pre_checkout(pre_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_q.id, ok=True)

# 📦 После оплаты
@dp.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    sp = message.successful_payment

    # Сохраняем в базу
    cursor.execute('''
        INSERT INTO payments (user_id, username, product_name, amount, currency, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        message.from_user.id,
        message.from_user.username,
        sp.invoice_payload,
        sp.total_amount / 100,
        sp.currency,
        "paid",
        datetime.now().isoformat()
    ))
    conn.commit()

    await message.answer(
        f"✅ Оплата прошла успешно!\n"
        f"Товар: {sp.invoice_payload}\n"
        f"Сумма: {sp.total_amount / 100} {sp.currency}"
    )

# ▶️ Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
