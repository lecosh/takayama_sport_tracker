from aiogram.filters import Command
from aiogram import types, F 
import emoji
from ..utils.constants import *

@dp.message(Command("standart"))
async def cmd_start(message: types.Message):
    """Handler for command "/standart". 
    This command suggest user different types of trains for various categiries.
    """
    kb = [
        [
            types.KeyboardButton(text="Похудение"),
            types.KeyboardButton(text="Поддержание формы"),
            types.KeyboardButton(text="Набор массы")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Выберите план", reply_markup=keyboard)

@dp.message(F.text == "Похудение")
async def weight_loss(message: types.Message):
    """Handler for button "Weight loss".
    That handler is the same as others handlers for 2 left categories. 
    """
    for day_plan in plan_for_weight_loss:
        await message.answer(day_plan, reply_markup=types.ReplyKeyboardRemove(), 
                             parse_mode=ParseMode.HTML)
    kb = [
        [
            types.KeyboardButton(text="Вернуться назад"),
            types.KeyboardButton(text="OK"),
            types.KeyboardButton(text="IMPORT")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Не забывайте про отдых между подходами и правильное питание", 
                         reply_markup=keyboard)

@dp.message(F.text == "Поддержание формы")
async def maintenance(message: types.Message):
    for day_plan in plan_for_maintenance:
        await message.answer(day_plan, reply_markup=types.ReplyKeyboardRemove(), 
                             parse_mode=ParseMode.HTML)
    kb = [
        [
            types.KeyboardButton(text="Вернуться назад"),
            types.KeyboardButton(text="OK"),
            types.KeyboardButton(text="IMPORT")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Не забывайте про отдых между подходами и правильное питание", 
                         reply_markup=keyboard)

@dp.message(F.text == "Набор массы")
async def muscle_gain(message: types.Message):
    for day_plan in plan_for_muscle_gain:
        await message.answer(day_plan, reply_markup=types.ReplyKeyboardRemove(), 
                             parse_mode=ParseMode.HTML)
    kb = [
        [
            types.KeyboardButton(text="Вернуться назад"),
            types.KeyboardButton(text="OK"),
            types.KeyboardButton(text="IMPORT")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Не забывайте про отдых между подходами и правильное питание", 
                         reply_markup=keyboard)

@dp.message(F.text == "Вернуться назад")
async def back(message: types.Message):
    await message.answer("Возвращение назад", reply_markup=types.ReplyKeyboardRemove())
    kb = [
        [
            types.KeyboardButton(text="Похудение"),
            types.KeyboardButton(text="Поддержание формы"),
            types.KeyboardButton(text="Набор массы")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Выберите план", reply_markup=keyboard)

@dp.message(F.text == "IMPORT")
async def import_smt(message: types.Message):
    await message.answer("Вы отправили IMPORT", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text == "OK")
async def import_smt(message: types.Message):
    await message.answer(emoji.emojize(":1st_place_medal:"), 
                         reply_markup=types.ReplyKeyboardRemove())