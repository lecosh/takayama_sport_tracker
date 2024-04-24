import telebot
from telebot import types
from aiogram import Router
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command 
from aiogram.types import ContentType
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
import openpyxl
import apiinfo
import sqlite3
import os
import aiosqlite
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile




router = Router()
bot = Bot(token=apiinfo.API_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
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
        [types.KeyboardButton(text="XLSX")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await msg.answer("Выберите формат: CSV или XLSX.\
                         \n\nНажмите на одну из кнопок ниже.", reply_markup=keyboard)
    
@dp.message(lambda message: message.text == "CSV" or message.text == "XLSX")
async def format_selected(msg: Message):
    if msg.text == "CSV":
        await msg.answer("Вы выбрали формат: CSV")
    elif msg.text == "XLSX":
        await msg.answer("Вы выбрали формат: XLSX. Пожалуйста, отправьте файл в этом формате.")


@dp.message(lambda message: message.document is not None)
async def handle_document(message: types.Message):
    await message.reply("Спасибо за отправку файла!")
    # Указываем более подходящую директорию для сохранения файлов
    # Например, папка 'downloads' в директории пользователя
    user_folder = os.path.expanduser('~')  # Получаем путь к домашней директории пользователя
    download_path = os.path.join(user_folder, 'downloads')

    # Проверяем, существует ли директория; если нет, создаем ее
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Путь, куда будет сохранён файл
    destination = os.path.join(download_path, message.document.file_name)

    # Получаем объект файла
    file_info = await bot.get_file(message.document.file_id)

    # Скачиваем файл
    await bot.download_file(file_info.file_path, destination)

    # Уведомляем пользователя о сохранении файла
    await message.reply(f"Файл был сохранен по пути: {destination}")
    user_id = message.from_user.id
    data = read_xlsx(destination)
    await save_to_db(user_id, data)

# Чтение данных из xlsx файла
def read_xlsx(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    data = []
    for row in sheet.iter_rows(min_row=2, max_col=7, values_only=True):
        data.append(list(row))
    return data

async def save_to_db(user_id, data):
    async with aiosqlite.connect('kl1de.db') as db:
        print(data)
        await db.execute('CREATE TABLE IF NOT EXISTS Trains (id INTEGER PRIMARY KEY, train TEXT)')
        cursor = await db.execute('SELECT id FROM Trains WHERE id = ?', (user_id,))
        if await cursor.fetchone():
            trains = ', '.join(data[0])  # предполагаем, что data[0] содержит нужные данные
            await db.execute('UPDATE Trains SET train = ? WHERE id = ?', (trains, user_id))
        else:
            trains = ', '.join(data[0])  # предполагаем, что data[0] содержит нужные данные
            await db.execute('INSERT INTO Trains (id, train) VALUES (?, ?)', (user_id, trains))
        await db.commit()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())