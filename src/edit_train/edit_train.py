from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram import types, F 
from aiogram.fsm.state import StatesGroup, State
from ..utils.constants import *
from ..utils.util import *


class Editing_train(StatesGroup):
    number_train = State()
    edit_or_delete = State()
    choose_action = State()


amount_train = 0
output = []
chosen_num = 0
async def push_new_train(state, msg):
    print(output)
    print(chosen_num)
    data = await state.get_data()
    trains = data["choosen_train"]
    trains = trains.lstrip('\n')  # remove leading newline character
    data_list = trains.split('\n')  # split the data into a list
    output[chosen_num - 1] = data_list
    output_str = ('\n' + '\n\n'.join(['\n'.join(block) for block in output]) + '\n') if output else ''
    await msg.answer("Отлично! Тренировка изменена")
    cursor.execute("UPDATE Trains SET train = ? WHERE id = ?", (output_str, msg.from_user.id))
    db.commit()
    await state.set_state(None)


async def read_train_db(msg):
    global amount_train
    global output
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

    amount_train = len(output)

    for i, block in enumerate(output, start=1):
        block_str = '\n'.join(block)
        await msg.answer(f"Тренировка {i}:\n{block_str}")
    await msg.answer("Введите номер тренировки:", reply_markup=types.ReplyKeyboardRemove())


@dp.message(StateFilter("Editing_train:number_train"))
async def choosing_num_train_handler(msg: Message, state: FSMContext):
    global chosen_num
    global amount_train
    global output
    chosen_num = int(msg.text)
    await state.set_state(Choosing_excersize.insert_state)
    await state.update_data(insert_flag=True)
    data = await state.get_data()
    print(data)
    if chosen_num > 0 and chosen_num <= amount_train:
        #del output[chosen_num - 1]  # remove the selected training block from output
        amount_train = len(output)
        await state.set_state(Editing_train.choose_action)
        exc_buttons = [
            [
                types.KeyboardButton(text="Удалить"),
                types.KeyboardButton(text="Изменить")
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=exc_buttons, resize_keyboard=True,
                                             input_field_placeholder="Выберите дальнейшее действие для упражнения...")
        await msg.answer(f"Выберите дальнейшее действие для упражнения...", reply_markup=keyboard)
    else:
        await msg.answer("Тренировки с таким номером нет...")
        await msg.answer("Попробуйте снова:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Editing_train.number_train)


@dp.message(F.text.lower() == "удалить",
            StateFilter("Editing_train:choose_action"))
async def choose_type(msg: types.Message, state: FSMContext):
    global output
    del output[chosen_num - 1]  # remove the selected training block from output
    #amount_train = len(output)
    output_str = ('\n' + '\n\n'.join(['\n'.join(block) for block in output]) + '\n') if output else ''
    print(output_str)
    await msg.answer("Отлично! Тренировка удалена")
    cursor.execute("UPDATE Trains SET train = ? WHERE id = ?", (output_str, msg.from_user.id))
    db.commit()
    await state.set_state(None)


@dp.message(F.text.lower() == "изменить",
            StateFilter("Editing_train:choose_action"))
async def choose_type(msg: types.Message, state: FSMContext):
    print(output)
    await state.set_state(Choosing_excersize.choosen_train)
    await state.update_data(choosen_train="")
    await state.set_state(Choosing_excersize.choose_creation_type)
    #await msg.answer(f"Выберите дальнейшее действие для упражнения...", reply_markup=types.ReplyKeyboardRemove())
    exc_buttons = [
        [
            types.KeyboardButton(text="Создать своё упражнение"),
            types.KeyboardButton(text="Выбрать существующее")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=exc_buttons, resize_keyboard=True,
                                         input_field_placeholder="Выберите дальнейшее действие для упражнения...")
    await msg.answer(f"Выберите дальнейшее действие для упражнения...", reply_markup=keyboard)


@dp.message(Command("edit_train"), StateFilter(None))
async def edit_handler(msg: Message, state: FSMContext):
    await state.set_state(Editing_train.number_train)
    data = await state.get_data()
    print(data)
    #await msg.answer(f"Выберите тренировку(введите номер тренировки):")
    #await state.set_state(Choosing_excersize.choose_creation_type)
    await read_train_db(msg)