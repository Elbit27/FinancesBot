import asyncio
import logging
import sys, django, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # Укажи путь к settings.py
django.setup()

from aiogram import Bot, Dispatcher, html, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from decouple import config
from category.models import Category
from asgiref.sync import sync_to_async
from report_daily.models import ReportDailyR


# Bot token can be obtained via https://t.me/BotFather
TOKEN = config('TOKEN_BOT')

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")



# Функция для получения категорий из базы
@sync_to_async
def get_categories():
    return [str(cat) for cat in Category.objects.all()]

@sync_to_async(thread_sensitive=True)
def save_expense(category, amount, body):
    print(f"Категория: {category}, Сумма: {amount}, Описание: {body}")  # Здесь можно добавить логику сохранения в БД


@sync_to_async
def save_expense(category_name, amount, body):
    try:
        category = Category.objects.get(name=category_name)  # Ищем категорию в базе
        expense = ReportDailyR(category=category, how_much=amount, body=body)
        expense.save()  # Сохраняем в базе
        return True
    except Category.DoesNotExist:
        return False

# --- FSM: Определение состояний ---
class ExpenseStates(StatesGroup):
    choosing_category = State()  # Ожидание выбора категории
    entering_body = State() # Ожидание ввода сообщения, на что именно потрачено (не обязательно)
    entering_amount = State()  # Ожидание ввода суммы


# --- Обработчик ввода "-" ---
@dp.message(F.text == "-")
async def choose_category(message: Message, state: FSMContext) -> None:
    cats = await get_categories()  # Загружаем категории
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cat)] for cat in cats],
        resize_keyboard=True
    )
    await message.reply('Выберите категорию расходов:', reply_markup=keyboard)
    await state.set_state(ExpenseStates.choosing_category)  # Устанавливаем состояние


# --- Обработчик выбора категории ---
@dp.message(ExpenseStates.choosing_category)
async def enter_amount(message: Message, state: FSMContext) -> None:
    category = message.text  # Сохраняем категорию
    await state.update_data(category=category)  # Запоминаем в состоянии
    await message.reply('Сколько вы потратили? Введите сумму:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(ExpenseStates.entering_amount)  # Ждем сумму


# --- Обработчик ввода суммы ---
@dp.message(ExpenseStates.entering_amount)
async def enter_body(message: Message, state: FSMContext) -> None:
    amount = message.text  # Получаем сумму
    if not amount.isdigit():  # Проверяем, что сумма числовая
        await message.reply("Введите корректную сумму!")
        return

    await state.update_data(amount=amount)  # Сохраняем сумму
    await message.reply("На что именно потратили?:")
    await state.set_state(ExpenseStates.entering_body)  # Ждем описание


# --- Обработчик ввода описания (body) ---
@dp.message(ExpenseStates.entering_body)
async def save_expense_handler(message: Message, state: FSMContext) -> None:
    body = message.text  # Получаем описание
    await state.update_data(body=body)  # Сохраняем описание

    user_data = await state.get_data()  # Получаем сохраненные данные
    category = user_data['category']
    amount = user_data['amount']

    # Сохранение в БД (замени print() на реальную логику)
    await save_expense(category, amount, body)

    await message.reply(f"✅ Записано: {amount} в категорию {category} \n📝 Описание: {body}")
    # print(amount, category, body)
    await state.clear()  # Сбрасываем состояние

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())