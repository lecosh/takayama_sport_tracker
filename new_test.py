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



class Choosing_excersize(StatesGroup):
    type_exc = State()
    number_exc = State()
    exc_reps = State()

train_list = ["Первая тренировка", "Вторая тренировка", "Третья тренировка"]




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
async def import_edit(msg: types.Message):
    kb = [
        [types.KeyboardButton(text=train_list[0])],
        [types.KeyboardButton(text=train_list[1])]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите тренировку:")
    await msg.answer(f"Выберите тренировку:", reply_markup=keyboard)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

