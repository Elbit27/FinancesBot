from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.database.db_utils import get_response


router = Router()

class ExpenseStates(StatesGroup):
    choosing_operation = State()  # Ожидание выбора категории



@router.message(Command('report'))  # Обработчик для команды report
async def report_d(message:Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cat)] for cat in ('доходы', 'расходы')],
        resize_keyboard=True
    )
    await message.answer('Вы желаете получить отчёт о доходах или расходах?', reply_markup=keyboard)
    await state.set_state(ExpenseStates.choosing_operation)  # Устанавливаем состояние


@router.message(ExpenseStates.choosing_operation)
async def get_report_handler(message: Message, state: FSMContext):
    report_list = await get_response()

    if not report_list:
        await message.answer("Нет данных в отчёте.")
    else:
        report_text = "\n".join(report_list)  # Объединяем список строк
        await message.answer(f"Вот отчёт:\n{report_text}")

    await state.clear()  # Сбрасываем состояние

