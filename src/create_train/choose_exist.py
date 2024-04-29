from aiogram import types, F 
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from ..utils.util import *
from ..utils.constants import *


@dp.message(F.text.lower() == "выбрать существующее", 
            StateFilter("Choosing_excersize:choose_creation_type"))
async def choose_type(msg: types.Message, state: FSMContext):
    type_exist_btns = [
        [types.KeyboardButton(text="Упражнения в тренажерах")],
        [types.KeyboardButton(text="Упражнения на время")],
        [types.KeyboardButton(text="Упражнения со своим весом")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=type_exist_btns, resize_keyboard=True, 
                                         input_field_placeholder="Выберите тип упражнения...")
    await msg.answer("Отлично!", reply_markup=types.ReplyKeyboardRemove())
    await msg.answer("Выберите тип существующего упражнения", reply_markup=keyboard)
    await state.set_state(Choosing_excersize.type_exc)


@dp.message(F.text.in_(available_type_excersize), 
            StateFilter("Choosing_excersize:type_exc"))
async def type_exc_handler(msg: types.Message, state: FSMContext):
    exc_str = ""
    if msg.text == available_type_excersize[0]:
        exc_str = create_list(machine_excersize)
    elif msg.text == available_type_excersize[1]:
        exc_str = create_list(time_excersize)
    else:
        exc_str = create_list(own_body_excersize)
    await msg.answer(f"Вот список \"{msg.text}\": {exc_str}", 
                    reply_markup=types.ReplyKeyboardRemove(),
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
                text=f"Спасибо. Вы выбрали \"{machine_excersize[number]}\". \
                Теперь, пожалуйста, выберите количество подходов.",
                input_field_placeholder="Введите количество подходов"
            )
            await state.set_state(Choosing_excersize.exc_reps)
        else:
            await msg.answer("Упражнения с таким номером нет...")
    elif type == "Упражнения на время":
        if number >= 0 and number <= len(time_excersize):
            await msg.answer(
                text=f"Спасибо. Вы выбрали \"{time_excersize[number]}\". \
                    Теперь, пожалуйста, выберите количество подходов.",
                input_field_placeholder="Введите количество подходов"
            )
            await state.set_state(Choosing_excersize.exc_reps)
        else:
            await msg.answer("Упражнения с таким номером нет...")
    else:
        if number >= 0 and number <= len(own_body_excersize):
            await msg.answer(
                text=f"Спасибо. Вы выбрали \"{own_body_excersize[number]}\". \
                    Теперь, пожалуйста, выберите количество подходов.",
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
        train = data["choosen_train"]
        # print(data)
        if type == "Упражнения в тренажерах":
            await msg.answer(f"Вы выбрали \"{machine_excersize[number]}\" на {reps} подход(ов)")
            await state.set_state(Choosing_excersize.choosen_train)
            await state.update_data(choosen_train=train + "\n" + machine_excersize[number] + " " + reps)
            await add_kb_next_exc(msg)
            await state.set_state(Choosing_excersize.add_next_exc)
        elif type == "Упражнения на время":
            await msg.answer(f"Вы выбрали \"{time_excersize[number]}\" на {reps} подход(ов)")
            await state.set_state(Choosing_excersize.choosen_train)
            await state.update_data(choosen_train=train + "\n" + machine_excersize[number]+ " " + reps)
            await add_kb_next_exc(msg)
            await state.set_state(Choosing_excersize.add_next_exc)
        else:
            await msg.answer(f"Вы выбрали \"{own_body_excersize[number]}\" на {reps} подход(ов)")
            await state.set_state(Choosing_excersize.choosen_train)
            await state.update_data(choosen_train=train + "\n" + machine_excersize[number]+ " " + reps)
            await add_kb_next_exc(msg)
            await state.set_state(Choosing_excersize.add_next_exc)
    else:
        await msg.answer("Количество подходов дожно быть меньше 20. Пожалейте себя...")
