from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.database.db_utils import get_report


router = Router()

class ExpensesStates(StatesGroup):
    choosing_operation = State()  # Ожидание выбора операции
    choosing_period = State()  # Ожидание выбора периода



@router.message(Command('report'))  # Обработчик для команды report
async def choose_operation(message:Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cat)] for cat in ('доходы', 'расходы')],
        resize_keyboard=True
    )
    await message.answer('Вы желаете получить отчёт о доходах или расходах?', reply_markup=keyboard)
    await state.set_state(ExpensesStates.choosing_operation)  # Устанавливаем состояние

# --- Обработчик ввода суммы ---
@router.message(ExpensesStates.choosing_operation)
async def choose_period(message: Message, state: FSMContext) -> None:
    operation = message.text
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cat)] for cat in ('день', 'неделя', 'месяц')],
        resize_keyboard=True
    )
    await state.update_data(operation=operation)  # Запоминаем в состоянии
    await message.answer('Выберите период:', reply_markup=keyboard)
    await state.set_state(ExpensesStates.choosing_period)  # Ждем выбора периода


@router.message(ExpensesStates.choosing_period)
async def get_report_handler(message: Message, state: FSMContext):
    period = message.text
    await state.update_data(period=period)  # Запоминаем в состоянии

    user_data = await state.get_data()  # Получаем сохраненные данные
    operation = user_data['operation']
    period = user_data['period']

    report_list = await get_report(operation, period)  # Запрашиваем отчёт из БД

    if not report_list:
        await message.answer("Нет данных в отчёте.")
    else:
        report_text = "\n".join(report_list)
        await message.answer(f"Вот отчёт за {period} по категории {operation}:\n{report_text}",
                             reply_markup=ReplyKeyboardRemove())

    await state.clear()  # Сбрасываем состояние