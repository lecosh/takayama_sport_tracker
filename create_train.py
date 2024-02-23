# -*- coding: utf-8 -*-
from aiogram.fsm.state import StatesGroup, State

from handlers import *
from constants import *

class Choosing_excersize(StatesGroup):
    choosing_excersize_number = State()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

router = Router()
bot = Bot(token=APY_KEY, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Это бот для трекинга спорта.")

# @dp.message(F.text.lower() == "создать своё упражнение")
# async def choose_existing_handler(message: types.Message):
#     await message.reply("Отличный выбор!")

@dp.message(F.text.lower() == "выбрать существующее")
async def without_puree(msg: types.Message):
    type_exist_btns = [
        [types.KeyboardButton(text="Упражнения в тренажерах")],
        [types.KeyboardButton(text="Упражнения на время")],
        [types.KeyboardButton(text="Упражнения со своим весом")]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=type_exist_btns, resize_keyboard=True, input_field_placeholder="Выберите тип упражнения...")
    await msg.answer("Отлично!", reply_markup=types.ReplyKeyboardRemove())
    await msg.answer("Выберите тип существующего упражнения", reply_markup=keyboard)

@dp.message(F.text.lower() == "упражнения в тренажерах", StateFilter(None))
async def without_puree(msg: types.Message, state: FSMContext):
    i = 1
    machine_excersize_str = "\n"
    for exc in machine_excersize:
        machine_excersize_str += str(i) + ") " + exc + "\n"
        i += 1
    await msg.answer(f"Вы выбрали упражнения в тренажерах! Вот список упражнений в тренажерах: {machine_excersize_str}", reply_markup=types.ReplyKeyboardRemove(),
                     input_field_placeholder="Введите номер упражнения...")
    await state.set_state(Choosing_excersize.choosing_excersize_number)

@dp.message(Choosing_excersize.choosing_excersize_number)
async def exc_choosen(msg: Message, state: FSMContext):
    await state.update_data(chosen_excersize=msg.text.lower())
    if int(msg.text.lower()) > 0 and int(msg.text.lower()) < len(machine_excersize):
        await msg.answer(
            text=f"Спасибо. Вы выбрали {machine_excersize[int(msg.text.lower())]}. Теперь, пожалуйста, выберите количество подходов:",
        )
    else:
        await msg.answer("Упражнения с таким номером нет...")



@dp.message(F.text.regexp(r'[1-7]'))
async def handle_amount(msg: Message):
    exc_buttons = [
        [
            types.KeyboardButton(text="Создать своё упражнение"),
            types.KeyboardButton(text="Выбрать существующее")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=exc_buttons, resize_keyboard=True, input_field_placeholder="Выберите дальнейшее действие для упражнения...")
    await msg.answer(f"Вы выбрали {msg.text} заняти(й/я).", reply_markup=keyboard)

# @router.message()
# async def message_handler(msg: Message):
#     await msg.answer(f"Твой ID: {msg.from_user.id}")


@dp.message(Command("create_train"))
async def create_train_handler(msg: Message):
    await msg.answer("Выберите количество тренировок в неделю: 1-7")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
