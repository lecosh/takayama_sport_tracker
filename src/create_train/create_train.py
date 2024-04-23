from aiogram import types, F 
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from ..utils.constants import *
from ..utils.util import *


"""Handler for next excersize.
This handler is triggered only if user choose one more excersize. Also state of bot
 is setting in "Choosing_excersize:add_next_exc".
"""
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
        await msg.answer("Для того, чтобы создать ещё одну тренировку введите /create_train", \
                         reply_markup=types.ReplyKeyboardRemove())
        await push_train_db(state, msg)
        await state.set_state(None)


"""Handler for "/create_train" command. 
Here the user is asked to choose one of two exercise choices. Here bot is setting in 
"Choosing_excersize:choose_creation_type" state. All states described in /src/utils/util.py
"""
@dp.message(Command("create_train"), StateFilter(None))
async def amount_handler(msg: Message, state: FSMContext):
    await state.set_state(Choosing_excersize.choosen_train)
    await state.update_data(choosen_train="")
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