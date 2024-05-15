from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram import types, F 
from aiogram.fsm.state import StatesGroup, State
from ..utils.constants import *
from ..utils.util import *


class EditingTrain(StatesGroup):
    number_train = State()
    edit_or_delete = State()
    choose_action = State()


async def push_new_train(state, msg):
    data = await state.get_data()
    trains = data.get("choosen_train", "")
    chosen_num = data.get("chosen_num", 0)
    output = data.get("output", [])

    trains = trains.lstrip('\n')
    data_list = trains.split('\n')
    output[chosen_num - 1] = data_list

    output_str = ('\n' + '\n\n'.join(['\n'.join(block) for block in output]) + '\n') if output else ''

    await msg.answer("Отлично! Тренировка изменена")
    cursor.execute("UPDATE Trains SET train = ? WHERE id = ?", (output_str, msg.from_user.id))
    db.commit()
    await state.clear()


async def read_train_db(msg, state):
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
    await state.update_data(output=output, amount_train=amount_train)

    for i, block in enumerate(output, start=1):
        block_str = '\n'.join(block)
        await msg.answer(f"Тренировка {i}:\n{block_str}")
    await msg.answer("Введите номер тренировки:", reply_markup=types.ReplyKeyboardRemove())


@dp.message(StateFilter("EditingTrain:number_train"))
async def choosing_num_train_handler(msg: Message, state: FSMContext):
    chosen_num = int(msg.text)
    data = await state.get_data()
    amount_train = data.get("amount_train", 0)
    await state.set_state(Choosing_excersize.insert_state)
    await state.update_data(insert_flag=True)
    data = await state.get_data()
    print(data)

    if 0 < chosen_num <= amount_train:
        await state.update_data(chosen_num=chosen_num)
        await state.set_state(EditingTrain.choose_action)

        exc_buttons = [
            [types.KeyboardButton(text="Удалить"), types.KeyboardButton(text="Изменить")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=exc_buttons, resize_keyboard=True,
                                             input_field_placeholder="Выберите дальнейшее действие для упражнения...")
        await msg.answer("Выберите дальнейшее действие для упражнения...", reply_markup=keyboard)
    else:
        await msg.answer("Тренировки с таким номером нет...")
        await msg.answer("Попробуйте снова:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(EditingTrain.number_train)


@dp.message(F.text.lower() == "удалить", StateFilter("EditingTrain:choose_action"))
async def delete_train_handler(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    output = data.get("output", [])
    chosen_num = data.get("chosen_num", 0)

    if 0 < chosen_num <= len(output):
        del output[chosen_num - 1]

        output_str = ('\n' + '\n\n'.join(['\n'.join(block) for block in output]) + '\n') if output else ''
        await msg.answer("Отлично! Тренировка удалена")
        cursor.execute("UPDATE Trains SET train = ? WHERE id = ?", (output_str, msg.from_user.id))
        db.commit()
        await state.clear()


@dp.message(F.text.lower() == "изменить", StateFilter("EditingTrain:choose_action"))
async def edit_train_handler(msg: types.Message, state: FSMContext):
    await state.update_data(choosen_train="")
    await state.set_state(Choosing_excersize.choose_creation_type)

    exc_buttons = [
        [types.KeyboardButton(text="Создать своё упражнение"), types.KeyboardButton(text="Выбрать существующее")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=exc_buttons, resize_keyboard=True,
                                         input_field_placeholder="Выберите дальнейшее действие для упражнения...")
    await msg.answer("Выберите дальнейшее действие для упражнения...", reply_markup=keyboard)


@dp.message(Command("edit_train"), StateFilter(None))
async def edit_handler(msg: Message, state: FSMContext):
    await state.set_state(EditingTrain.number_train)
    await read_train_db(msg, state)