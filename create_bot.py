from aiogram import Bot, Dispatcher, types

git config --list | grep user.nameasync_bot = Bot(token=BOT_TOKEN,parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=async_bot)