from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import *


async_bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=async_bot)


@dp.message_handler(content_types=["sticker"])
async def get_sticker(message):
    print(message.sticker.file_id)
    await async_bot.send_message(message.chat.id, message.sticker.file_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)