from aiogram import Router
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import regexp
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import config
from ..utils.util import *



amount_train = 0

async def read_train_db(msg):
    """Adding train in database.
    Different trains separates in database with "\n" symbol.
    Note: while parsing trains for import trains, pay attention on following separation.
    """
    cursor.execute("SELECT train FROM Trains WHERE id = ?", (msg.from_user.id,))
    row = cursor.fetchone()
    output = []
    temp = []
    for line in row[0].split('\n'):
        if line:
            temp.append(line)
        else:
            if temp:
                output.append(temp)
                temp = []
    if temp:
        output.append(temp)

    for i, block in enumerate(output, start=1):
        block_str = '\n'.join(block)
        await msg.answer(f"Тренировка {i}:\n{block_str}")
    await msg.answer("Введите номер тренировки:", reply_markup=types.ReplyKeyboardRemove())
    amount_train = i - 1


   # print('\n'.join(output))
    print(row[0])
    print(output)
    #train_data = str(row[0]) + trains + "\n"
    #cursor.execute("UPDATE Trains SET train = ? WHERE id = ?", (train_data, msg.from_user.id))
    #db.commit()


@dp.message(Choosing_excersize.number_train)
async def choosing_num_train_handler(msg: Message, state: FSMContext):
    if int(msg.text) > 0 and int(msg.text) <= 20:
        await state.update_data(choosen_reps=msg.text.lower())
        data = await state.get_data()
        type = data["choosen_type"]
        number = data["choosen_number"]


class Choosing_excersize(StatesGroup):
    type_exc = State()
    number_exc = State()
    exc_reps = State()






router = Router()
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

@router.message(Command("start"))
async def start_handler(msg:Message):
    await msg.answer("Сегодня мы будем готовить мои любимые фритату-та-ту-та-ту. Для просмотра команд введите /info.")


@dp.message(Command("info"))
async def info_handler(msg:Message):
    await  msg.answer("Доступные комманды:\n/create_train - Создать тренировку.\
                         \n/choose_standart_train - Выбрать тренировку из списка стандартных.\
                         \n/import_your_train - Импортировать свою тренировку. \
                         \n/edit_train - Редактировать тренировку.")


train_list = ["первая трренировка"]
@dp.message(F.text.in_(train_list), StateFilter(None))
async def print_train(msg: types.Message, state: FSMContext):
    await msg.answer(f"Происходит вывод выбранной тренировки", reply_markup=types.ReplyKeyboardRemove())
    kb = [
        [types.KeyboardButton(text="Удалить")],
        [types.KeyboardButton(text="Изменить")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         input_field_placeholder="Выберите действие над тренировкой:")
    await msg.answer(f"Выберите действие над тренировкой:", reply_markup=keyboard)

    #await msg.answer("происходит вывод выбранной тренировки")
    # data = await state.get_data()
    # print(data)


@dp.message(Command("import_your_train"))
async def import_handler(msg: types.Message):
    kb = [
        types.KeyboardButton(text="CSV"),
        types.KeyboardButton(text="XLS")
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await msg.answer("Выберите формат: CSV или XLS. \n\nНажмите на одну из кнопок ниже.", reply_markup=keyboard)


@dp.message(Command("edit_train"))
async def import_edit(msg: types.Message, state: FSMContext):
    await state.set_state(Choosing_excersize.number_train)
    #await msg.answer(f"Выберите тренировку(введите номер тренировки):")
    #await state.set_state(Choosing_excersize.choose_creation_type)
    await read_train_db(msg)




async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

