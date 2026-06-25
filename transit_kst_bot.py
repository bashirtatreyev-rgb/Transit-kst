"""
Transit KST - Telegram Bot (Aiogram 3)
ransiimport asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8764057153:AAFZM-E7F_E9NaPK6ZpXKa5G0SyZGz0CsFo"

ADMIN_ID = 6230694331

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class RequestForm(StatesGroup):
    transport = State()
    city_from = State()
    city_to = State()
    phone = State()


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Оставить заявку")],
        [KeyboardButton(text="🚛 Найти транспорт")],
        [KeyboardButton(text="☎️ Контакты")]
    ],
    resize_keyboard=True
)

transport_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚐 Газель"), KeyboardButton(text="📏 Длинномер")],
        [KeyboardButton(text="🚛 Фура"), KeyboardButton(text="🇪🇺 Еврофура")],
        [KeyboardButton(text="🚜 Трал"), KeyboardButton(text="🚚 HOWO")],
        [KeyboardButton(text="🏗 Манипулятор"), KeyboardButton(text="🚚 Самосвал")],
        [KeyboardButton(text="⚙️ Спецтехника")]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🚚 Transit KST\n\nБиржа грузоперевозок и спецтехники.",
        reply_markup=main_kb
    )


@dp.message(F.text.in_(["📦 Оставить заявку", "🚛 Найти транспорт"]))
async def create_request(message: Message, state: FSMContext):
    await state.set_state(RequestForm.transport)
    await message.answer("Выберите транспорт:", reply_markup=transport_kb)


@dp.message(RequestForm.transport)
async def transport(message: Message, state: FSMContext):
    await state.update_data(transport=message.text)
    await state.set_state(RequestForm.city_from)
    await message.answer("Укажите город загрузки:")


@dp.message(RequestForm.city_from)
async def city_from(message: Message, state: FSMContext):
    await state.update_data(city_from=message.text)
    await state.set_state(RequestForm.city_to)
    await message.answer("Укажите город выгрузки:")


@dp.message(RequestForm.city_to)
async def city_to(message: Message, state: FSMContext):
    await state.update_data(city_to=message.text)
    await state.set_state(RequestForm.phone)
    await message.answer("Введите номер телефона:")


@dp.message(RequestForm.phone)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()

    text = f"""
🚚 НОВАЯ ЗАЯВКА

Транспорт: {data['transport']}
Откуда: {data['city_from']}
Куда: {data['city_to']}
Телефон: {data['phone']}

User ID: {message.from_user.id}
Username: @{message.from_user.username or 'нет'}
"""

    await bot.send_message(ADMIN_ID, text)
    await message.answer("✅ Заявка отправлена. Мы свяжемся с вами.")
    await state.clear()


@dp.message(F.text == "☎️ Контакты")
async def contacts(message: Message):
    await message.answer(
        "☎️ Контакты\n\nУкажите здесь номер телефона и ссылку на ваш канал."
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
