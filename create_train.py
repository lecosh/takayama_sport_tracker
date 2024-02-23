# -*- coding: utf-8 -*-

from handlers import *
from constants import *

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

router = Router()
bot = Bot(token=APY_KEY, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")

@dp.message(F.text.regexp(r'[1-7]'))
async def handle_amount(msg: Message):
    await msg.answer(msg.text)

@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")


@dp.message(Command("create_train"))
async def create_train_handler(msg: Message):
    await msg.answer("Выберите количество тренировок в неделю: 1-7")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
