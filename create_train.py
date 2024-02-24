# -*- coding: utf-8 -*-
from aiogram.fsm.state import StatesGroup, State
import sqlite3

from handlers import *
from constants import *

def create_list(exc_type):
    i = 1
    excersize_str = "\n"
    for exc in exc_type:
        excersize_str += str(i) + ") " + exc + "\n"
        i += 1
    return excersize_str

async def add_kb_next_exc(msg):
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await msg.answer("Добавить ещё одно упражнение?", reply_markup=keyboard)

class Choosing_excersize(StatesGroup):
    type_exc = State() #тип сущетсувующшего упражнения
    number_exc = State() #порядковый номер упражнения в массиве
    exc_reps = State() #количество подходов в упражнении
    add_next_exc = State() #добавить новое упражнение или нет
    choose_creation_type = State() #выбор типа добавляемого упражнения

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

router = Router()
bot = Bot(token=APY_KEY, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)
db = sqlite3.connect('my_database.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS trains(id INTEGER, train TEXT)")
db.commit()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Это бот для трекинга спорта.")

@dp.message(F.text.lower() == "выбрать существующее", StateFilter("Choosing_excersize:choose_creation_type"))
async def choose_type(msg: types.Message, state: FSMContext):
    type_exist_btns = [
        [types.KeyboardButton(text="Упражнения в тренажерах")],
        [types.KeyboardButton(text="Упражнения на время")],
        [types.KeyboardButton(text="Упражнения со своим весом")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=type_exist_btns, resize_keyboard=True, input_field_placeholder="Выберите тип упражнения...")
    await msg.answer("Отлично!", reply_markup=types.ReplyKeyboardRemove())
    await msg.answer("Выберите тип существующего упражнения", reply_markup=keyboard)
    await state.set_state(Choosing_excersize.type_exc)

@dp.message(F.text.in_(available_type_excersize), StateFilter("Choosing_excersize:type_exc"))
async def type_exc_handler(msg: types.Message, state: FSMContext):
    exc_str = ""
    if msg.text == available_type_excersize[0]:
        exc_str = create_list(machine_excersize)
    elif msg.text == available_type_excersize[1]:
        exc_str = create_list(time_excersize)
    else:
        exc_str = create_list(own_body_excersize)
    await msg.answer(f"Вот список \"{msg.text}\": {exc_str}", reply_markup=types.ReplyKeyboardRemove(),
                     input_field_placeholder="Введите номер упражнения...")
    await state.update_data(choosen_type=msg.text)
    await state.set_state(Choosing_excersize.number_exc)

@dp.message(Choosing_excersize.number_exc)
async def number_exc_validation_handler(msg: Message, state: FSMContext):
    await state.update_data(choosen_number=int(msg.text.lower()) - 1)
    data = await state.get_data()
    type = data["choosen_type"]
    number = data["choosen_number"]
    print(data)
    if type == "Упражнения в тренажерах":
        if number >= 0 and number <= len(machine_excersize):
            await msg.answer(
                text=f"Спасибо. Вы выбрали \"{machine_excersize[number]}\". Теперь, пожалуйста, выберите количество подходов.",
                input_field_placeholder="Введите количество подходов"
            )
            await state.set_state(Choosing_excersize.exc_reps)
        else:
            await msg.answer("Упражнения с таким номером нет...")
    elif type == "Упражнения на время":
        if number >= 0 and number <= len(time_excersize):
            await msg.answer(
                text=f"Спасибо. Вы выбрали \"{time_excersize[number]}\". Теперь, пожалуйста, выберите количество подходов.",
                input_field_placeholder="Введите количество подходов"
            )
            await state.set_state(Choosing_excersize.exc_reps)
        else:
            await msg.answer("Упражнения с таким номером нет...")
    else:
        if number >= 0 and number <= len(own_body_excersize):
            await msg.answer(
                text=f"Спасибо. Вы выбрали \"{own_body_excersize[number]}\". Теперь, пожалуйста, выберите количество подходов.",
                input_field_placeholder="Введите количество подходов"
            )
            await state.set_state(Choosing_excersize.exc_reps)
        else:
            await msg.answer("Упражнения с таким номером нет...")

@dp.message(Choosing_excersize.exc_reps)
async def choosing_reps_handler(msg: Message, state: FSMContext):
    if int(msg.text) > 0 and int(msg.text) <= 20:
        await state.update_data(choosen_reps=msg.text.lower())
        data = await state.get_data()
        type = data["choosen_type"]
        number = data["choosen_number"]
        reps = data["choosen_reps"]
        print(data)
        if type == "Упражнения в тренажерах":
            await msg.answer(f"Вы выбрали \"{machine_excersize[number]}\" на {reps} подход(ов)")
            await add_kb_next_exc(msg)
            await state.set_state(Choosing_excersize.add_next_exc)
            cursor.execute("INSERT INTO trains (id, train) VALUES (?, ?)", (msg.from_user.id, machine_excersize[number] + " " + reps))
            db.commit()
        elif type == "Упражнения на время":
            await msg.answer(f"Вы выбрали \"{time_excersize[number]}\" на {reps} подход(ов)")
            await add_kb_next_exc(msg)
            await state.set_state(Choosing_excersize.add_next_exc)
        else:
            await msg.answer(f"Вы выбрали \"{own_body_excersize[number]}\" на {reps} подход(ов)")
            await add_kb_next_exc(msg)
            await state.set_state(Choosing_excersize.add_next_exc)
    else:
        await msg.answer("Количество подходов дожно быть меньше 20. Пожалейте себя...")


@dp.message(F.text.in_(add_next_excersize), StateFilter("Choosing_excersize:add_next_exc"))
async def handle_next_exc_choose(msg: Message, state: FSMContext):
    if msg.text == 'Да':
        await state.set_state(Choosing_excersize.choose_creation_type)
        exc_buttons = [
            [
                types.KeyboardButton(text="Создать своё упражнение"),
                types.KeyboardButton(text="Выбрать существующее")
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=exc_buttons, resize_keyboard=True,
                                             input_field_placeholder="Выберите дальнейшее действие для упражнения...")
        await msg.answer(f"Выберите дальнейшее действие для упражнения...", reply_markup=keyboard)
    elif msg.text == 'Нет':
        pass

@dp.message(F.text.regexp(r'([1-7])'), StateFilter("Choosing_excersize:choose_creation_type"))
async def amount_handler(msg: Message, state: FSMContext):
    exc_buttons = [
        [
            types.KeyboardButton(text="Создать своё упражнение"),
            types.KeyboardButton(text="Выбрать существующее")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=exc_buttons, resize_keyboard=True, input_field_placeholder="Выберите дальнейшее действие для упражнения...")
    await msg.answer(f"Выберите дальнейшее действие для упражнения...", reply_markup=keyboard)

# @router.message()
# async def message_handler(msg: Message):
#     await msg.answer(f"Твой ID: {msg.from_user.id}")

@dp.message(Command("create_train"), StateFilter(None))
async def create_train_handler(msg: Message, state: FSMContext):
    await state.set_state(Choosing_excersize.choose_creation_type)
    await msg.answer("Выберите количество тренировок в неделю: 1-7")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
