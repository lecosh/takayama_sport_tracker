from aiogram.filters import Command
from ..utils.constants import *
from ..utils.util import *


@dp.message(Command("get_trains"))
async def handle_get_trains(msg: types.Message):
    cursor.execute("SELECT train FROM TRAINS WHERE ID = ?", (msg.from_user.id,))

    rows = cursor.fetchall()
    
    result_list = [row[0] for row in rows]
    print(f"result LIST {result_list}")
    if len(result_list[0]) == 0:
        await msg.answer('Тренировок нет')
    else:
        split_result = []
        for train in result_list:
            split_train = train.split('\n\n')
            split_result.extend([part.strip() for part in split_train])
        count = 1
        for train in split_result:
            await msg.answer(f'<b>Тренировка {count}</b>:', parse_mode=ParseMode.HTML)
            await msg.answer(train)
            count += 1