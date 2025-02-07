from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from bot.database.db_utils import get_income_categories, save_incomes

router = Router()

# --- FSM: Определение состояний ---
class ExpensesStates(StatesGroup):
    choosing_category_income = State()  # Ожидание выбора категории
    entering_body_income = State() # Ожидание ввода сообщения, на что именно потрачено (не обязательно)
    entering_amount_income = State()  # Ожидание ввода суммы



# --- Обработчик ввода "+" ---
@router.message(F.text == "+")
async def choose_category(message: Message, state: FSMContext) -> None:
    cats = await get_income_categories()  # Загружаем категории
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cat)] for cat in cats],
        resize_keyboard=True
    )
    await message.reply('Выберите категорию доходов:', reply_markup=keyboard)
    await state.set_state(ExpensesStates.choosing_category_income)  # Устанавливаем состояние


# --- Обработчик выбора категории ---
@router.message(ExpensesStates.choosing_category_income)
async def enter_amount(message: Message, state: FSMContext) -> None:
    category = message.text  # Сохраняем категорию
    await state.update_data(category=category)  # Запоминаем в состоянии
    await message.reply('На сколько увеличился ваш баланс? Введите сумму:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(ExpensesStates.entering_amount_income)  # Ждем сумму


# --- Обработчик ввода суммы ---
@router.message(ExpensesStates.entering_amount_income)
async def enter_body(message: Message, state: FSMContext) -> None:
    amount = message.text  # Получаем сумму
    if not amount.isdigit():  # Проверяем, что сумма числовая
        await message.reply("Введите корректную сумму!")
        return

    await state.update_data(amount=amount)  # Сохраняем сумму
    await message.reply("Пару слов туда сюда подробнее:")
    await state.set_state(ExpensesStates.entering_body_income)  # Ждем описание


# --- Обработчик ввода описания (body) ---
@router.message(ExpensesStates.entering_body_income)
async def save_income_handler(message: Message, state: FSMContext) -> None:
    body = message.text  # Получаем описание
    await state.update_data(body=body)  # Сохраняем описание

    user_data = await state.get_data()  # Получаем сохраненные данные
    category = user_data['category']
    amount = user_data['amount']

    # Сохранение в БД (замени print() на реальную логику)
    await save_incomes(category, amount, body)

    await message.reply(f"✅ Записано: {amount} сом в категорию {category} \n📝 Описание: {body}")
    # print(amount, category, body)
    await state.clear()  # Сбрасываем состояние