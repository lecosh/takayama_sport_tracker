import asyncio
import logging

from src.utils.constants import *
from src.utils.util import *
from src.create_train.create_exc import *
from src.create_train.choose_exist import *
from src.create_train.create_train import *


@dp.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer("Привет!")
    cursor.execute("INSERT OR REPLACE INTO Trains (id, train) VALUES (?, ?)", (msg.from_user.id, ""))
    db.commit()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())