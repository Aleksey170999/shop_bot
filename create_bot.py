from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

BOT_TOKEN = "2098590577:AAGE3dldlvESt2ieqImgPl1s8zFjIzRrkp4"


storage = MemoryStorage()


async_bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=async_bot, storage=storage)
