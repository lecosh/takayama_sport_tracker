from aiogram import types, F 
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from ..utils.constants import *
from ..utils.util import *


@dp.message(F.text.lower() == "создать своё упражнение", 
            StateFilter("Choosing_excersize:choose_creation_type"))
async def choose_type(msg: types.Message, state: FSMContext):
    """Handler for createing own excersize. 
    Format of user message isn't validating. After user message bot is setting in 
    "Choosing excersize:own_excersize" state.
    """
    await msg.answer("Отлично! Опишите своё упражнение (название, количество подходов)", 
                     reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Choosing_excersize.own_excersize)


@dp.message(StateFilter("Choosing_excersize:own_excersize"))
async def message_handler(msg: Message, state: FSMContext):
    """Handler for user own excersize. 
    After that bot is setting in "Choosing_excersize:add_next_exc" state.
    """
    await msg.answer("Отлично, это упражнение будет добавлено в базу данных")
    await state.set_state(Choosing_excersize.choosen_train)
    data = await state.get_data()
    train = data["choosen_train"]
    await state.update_data(choosen_train=train + "\n" + msg.text)
    await add_kb_next_exc(msg)
    await state.set_state(Choosing_excersize.add_next_exc)