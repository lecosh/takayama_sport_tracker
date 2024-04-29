from aiogram.filters import Command
from aiogram.types import Message
from ..utils.constants import *


@dp.message(Command("help"))
async def info_handler(msg:Message):
    await msg.answer("Доступные команды:\n/create_train - Создать тренировку\
                        \n/choose_standart_train - Выбрать тренировку из списка стандартных\
                        \n/import_train - Импортировать свою тренировку\
                        \n/edit_train - Редактировать тренировку\
                        \n/get_trains - Список созданных тренировок\
                        \n/help - Список доступных команд")