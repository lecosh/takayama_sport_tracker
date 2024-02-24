import telebot

from telebot import types
from aiogram import Router
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import config

router = Router()
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

@router.message(Command("start"))
async def start_handler(msg:Message):
    await msg.answer("Введите /info для просмотра справки доступных команд")


@dp.message(Command("info"))
async def info_handler(msg:Message):
    await  msg.answer("Доступные комманды:\n/edit_train - Позволяет отредактировать выбранную тренировку.\
                         \n/create_train - Создать тренировку.\
                         \n/choose_standart_train - Выбрать тренировку из списка стандартных.\
                         \n/import_your_train - Импортировать свою тренировку")


@dp.message(Command("import_your_train"))
async def import_handler(msg:Message):
    kb = [
        [types.KeyboardButton(text="CSV")],
        [types.KeyboardButton(text="XLS")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await msg.answer("Выберите формат: CSV или XLS.\
                         \n\nНажмите на одну из кнопок ниже.", reply_markup=keyboard)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

