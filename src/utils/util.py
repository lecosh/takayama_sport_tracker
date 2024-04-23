from aiogram.fsm.state import StatesGroup, State
from aiogram import types
from ..utils.constants import *

def create_list(exc_type):
    i = 1
    excersize_str = "\n"
    for exc in exc_type:
        excersize_str += str(i) + ") " + exc + "\n"
        i += 1
    return excersize_str

async def push_train_db(state, msg):
    cursor.execute("SELECT train FROM Trains WHERE id = ?", (msg.from_user.id,))
    data = await state.get_data()
    trains = data["choosen_train"]
    row = cursor.fetchone()
    print(row[0])
    str = row[0] + trains + "\n"
    cursor.execute("UPDATE Trains SET train = ? WHERE id = ?", (str, msg.from_user.id))
    db.commit()

class Choosing_excersize(StatesGroup):
    type_exc = State() #тип сущетсувующшего упражнения
    number_exc = State() #порядковый номер упражнения в массиве
    exc_reps = State() #количество подходов в упражнении
    add_next_exc = State() #добавить новое упражнение или нет
    choose_creation_type = State() #выбор типа добавляемого упражнения
    choosen_train = State()
    own_excersize = State()

async def add_kb_next_exc(msg):
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await msg.answer("Добавить ещё одно упражнение?", reply_markup=keyboard)