import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties

import config

plan_for_weight_loss = [
    "<b>Понедельник</b>:\n- <b>Кардио:</b> 45 минут бега трусцой или плавания.\n- <b>Силовые тренировки:</b> Комплекс на все тело (3 подхода по 10-12 повторений каждого упражнения):\n  - Приседания\n  - Выпады\n  - Отжимания\n  - Становая тяга с легким весом\n  - Жим гантелей над головой",
    "<b>Вторник</b>:\n- <b>Кардио:</b> 30 минут езды на велосипеде\n- <b>Интервальные тренировки:</b> Высокоинтенсивные интервальные тренировки (HIIT) в течение 20 минут.",
    "<b>Среда</b>:\n- <b>Отдых:</b> Легкая растяжка или йога",
    "<b>Четверг</b>:\n- <b>Кардио:</b> 45 минут на эллиптическом тренажере\n- <b>Силовые тренировки:</b> Комплекс на все тело (3 подхода по 10-12 повторений каждого упражнения):\n  - Подтягивания\n  - Планка\n  - Бицепс с гантелями\n  - Разгибание рук с гантелями\n  - Подъемы на носки",
    "<b>Пятница</b>:\n- <b>Кардио:</b> 45 минут ходьбы\n- <b>Интервальные тренировки:</b> Высокоинтенсивные интервальные тренировки (HIIT) в течение 20 минут.",
    "<b>Суббота</b>:\n- <b>Активный отдых:</b> Легкая активность, например, прогулка или йога",
    "<b>Воскресенье</b>:\n- <b>Отдых:</b> Отдых или легкая активность"
]

plan_for_muscle_gain = [
    "<b>Понедельник</b>:\n- <b>Грудь и трицепсы:</b>\n  - Жим лежа (4 подхода по 8-10 повторений).\n  - Разводка гантелей лежа (4 подхода по 10-12 повторений).\n  - Отжимания на брусьях (3 подхода по 8-10 повторений).\n  - Разгибания рук с гантелями (3 подхода по 10-12 повторений).",
    "<b>Вторник</b>:\n- <b>Спина и бицепсы:</b>\n  - Тяга штанги к поясу (4 подхода по 8-10 повторений).\n  - Подтягивания (3 подхода по 8-10 повторений).\n  - Подъемы штанги на бицепс (3 подхода по 10-12 повторений).\n  - Сгибания рук с гантелями (3 подхода по 10-12 повторений).",
    "<b>Среда</b>:\n- <b>Отдых:</b> Легкая активность или растяжка",
    "<b>Четверг</b>:\n- <b>Ноги и плечи:</b>\n  - Приседания со штангой (4 подхода по 8-10 повторений).\n  - Жим ногами (3 подхода по 10-12 повторений).\n  - Жим гантелей сидя (3 подхода по 8-10 повторений).\n  - Подъемы на носки (3 подхода по 12-15 повторений).",
    "<b>Пятница</b>:\n- <b>Отдых:</b> Легкая активность или растяжка",
    "<b>Суббота</b>:\n- <b>Восстановление:</b> Легкая активность или отдых",
    "<b>Воскресенье</b>:\n- <b>Отдых:</b> Легкая активность или отдых"
]

plan_for_maintenance = [
    "<b>Понедельник</b>:\n- <b>Кардио:</b> 30 минут бега или езды на велосипеде\n- Комплекс на все тело (3 подхода по 10-12 повторений каждого упражнения):\n  - Приседания\n  - Выпады\n  - Отжимания\n  - Подтягивания",
    "<b>Вторник</b>:\n- <b>Йога или пилатес:</b> 45 минут для улучшения гибкости и растяжки",
    "<b>Среда</b>:\n- <b>Кардио:</b> 30 минут на эллиптическом тренажере или плавания\n- <b>Комплекс на все тело</b> (3 подхода по 10-12 повторений каждого упражнения):\n  - Жим гантелей над головой\n  - Бицепс с гантелями\n  - Разгибание рук с гантелями\n  - Подъемы на носки",
    "<b>Четверг</b>:\n- <b>Активный отдых:</b> Легкая активность, например, йога или прогулка",
    "<b>Пятница</b>:\n- <b>Кардио:</b> 30 минут езды на велосипеде или ходьбы\n- Комплекс на все тело (3 подхода по 10-12 повторений каждого упражнения):\n  - Планка\n  - Подъем ног в висе\n  - Становая тяга с легким весом\n  - Жим ногами",
    "<b>Суббота</b>:\n- <b>Активный отдых:</b> Легкая активность или отдых",
    "<b>Воскресенье</b>:\n- <b>Отдых:</b> Отдых или легкая активность"
]


router = Router()
bot = Bot(token=config.API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
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
    for day_plan in plan_for_weight_loss:
        await message.answer(day_plan, reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    kb = [
        [
            types.KeyboardButton(text="Вернуться назад"),
            types.KeyboardButton(text="ОК"),
            types.KeyboardButton(text="IMPORT")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Не забывайте про отдых между подходами и правильное питание", reply_markup=keyboard)

@dp.message(F.text == "Поддержание формы")
async def maintenance(message: types.Message):
    for day_plan in plan_for_maintenance:
        await message.answer(day_plan, reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    kb = [
        [
            types.KeyboardButton(text="Вернуться назад"),
            types.KeyboardButton(text="ОК"),
            types.KeyboardButton(text="IMPORT")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Не забывайте про отдых между подходами и правильное питание", reply_markup=keyboard)

@dp.message(F.text == "Набор массы")
async def muscle_gain(message: types.Message):
    for day_plan in plan_for_muscle_gain:
        await message.answer(day_plan, reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    kb = [
        [
            types.KeyboardButton(text="Вернуться назад"),
            types.KeyboardButton(text="ОК"),
            types.KeyboardButton(text="IMPORT")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Не забывайте про отдых между подходами и правильное питание", reply_markup=keyboard)

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
    await message.answer("Вы отправили OK", reply_markup=types.ReplyKeyboardRemove())

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())