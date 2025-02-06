import asyncio
import logging
import sys, django, os

# Нужная штука:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # Укажу путь к settings.py
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config
from bot.handlers import start, expense, report


# Bot token can be obtained via https://t.me/BotFather
TOKEN = config('TOKEN_BOT')

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(expense.router)
    dp.include_router(report.router)

    # And the run events dispatching
    await dp.start_polling(bot)





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())