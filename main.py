import asyncio
import logging
from src.utils.constants import *
from src.utils.util import *
from src.create_train.create_exc import *
from src.create_train.choose_exist import *
from src.create_train.create_train import *
from src.standart_train.stand_train import *
from src.edit_train.edit_train import *
from src.get_trains.get_trains import *
from src.helper.help import *


@dp.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    """Starting bot. 
    Note: user will be added in database only if command "/start" will be triggered
    """
    await msg.answer(f"Привет, {msg.from_user.first_name}! Это бот для фитнес-трекинга.\n"
                    "Чтобы посмотреть список доступных команд, введи /help.")
    cursor.execute("INSERT OR REPLACE INTO Trains (id, train) VALUES (?, ?)", 
                   (msg.from_user.id, ""))
    db.commit()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())