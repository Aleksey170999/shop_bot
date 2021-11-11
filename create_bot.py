from aiogram import Bot, Dispatcher, types

BOT_TOKEN = "123"
async_bot = Bot(token=BOT_TOKEN,parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=async_bot)


