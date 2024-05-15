from aiogram import types, F 
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from ..edit_train.edit_train import push_new_train
from ..utils.constants import *
from ..utils.util import *


@dp.message(F.text.in_(add_next_excersize), StateFilter("Choosing_excersize:add_next_exc"))
async def handle_next_exc_choose(msg: Message, state: FSMContext):
    """Handler for next excersize.
    This handler is triggered only if user choose one more excersize. Also state of bot
    is setting in "Choosing_excersize:add_next_exc".
    """
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
        data = await state.get_data()
        if data.get('insert_flag') == False:
            await push_train_db(state, msg)
        else:
            await push_new_train(state, msg)
        await state.set_state(None)


@dp.message(Command("create_train"), StateFilter(None))
async def amount_handler(msg: Message, state: FSMContext):
    """Handler for "/create_train" command. 
    Here the user is asked to choose one of two exercise choices. Here bot is setting in 
    "Choosing_excersize:choose_creation_type" state. All states described in /src/utils/util.py
    """
    await state.set_state(Choosing_excersize.choosen_train)
    await state.update_data(choosen_train="")
    await state.set_state(Choosing_excersize.insert_state)
    await state.update_data(insert_flag=False)
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