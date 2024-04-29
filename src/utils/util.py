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
    """Adding train in database.
    Different trains separates in database with "\n" symbol. 
    Note: while parsing trains for import trains, pay attention on following separation.
    """
    cursor.execute("SELECT train FROM Trains WHERE id = ?", (msg.from_user.id,))
    data = await state.get_data()
    trains = data["choosen_train"]
    row = cursor.fetchone()
    print(row[0])
    str = row[0] + trains + "\n"
    cursor.execute("UPDATE Trains SET train = ? WHERE id = ?", (str, msg.from_user.id))
    db.commit()


class Choosing_excersize(StatesGroup):
    """This is class containing differrent states of bot when user creating excersizes for train.
    This states is used only in "/create_train" command, each state trigger different stages 
    of creating an excersize.
    """
    type_exc = State() #typer of an existing excersize
    number_exc = State() #number of excersize in array
    exc_reps = State() #amount of reps in excersize
    add_next_exc = State() #adding new excersize
    choose_creation_type = State() #choose type of added excersize
    choosen_train = State() #picked train
    own_excersize = State()
    insert_state = State()


async def add_kb_next_exc(msg):
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await msg.answer("Добавить ещё одно упражнение?", reply_markup=keyboard)