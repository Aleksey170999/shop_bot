import logging
from asycnconf import asbot, async_bot, scheme, PHONE, cursor, QIWI
from aiogram import executor
from aiogram.types import *
from markup import *
from db import db
from pyqiwip2p import QiwiP2P
from aiogram.dispatcher.filters import Text
from random import randint


logging.basicConfig(level=logging.INFO)


def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False


@asbot.message_handler(commands=['start'])
async def register(message: Message):
    if not is_number(message.text):
        if message.chat.type == "private":
            if not db.user_exists(message.from_user.id):
                db.create_user(message.from_user.id, message.from_user.username, wallet=0)
                await message.reply("Добро пожаловать, вы успешно зарегистрировались в боте.")
            await message.reply("Выберите что-нибудь", reply_markup=main_markup)


@asbot.message_handler(Text(equals="Категории"))
async def handle_nav(message: Message):
    if not is_number(message.text):
        await message.delete()
        await async_bot.send_message(message.from_user.id, "Категории:", reply_markup=VV_50_markup)


@asbot.message_handler(Text(equals="Профиль"))
async def profile(message: Message):
    if not is_number(message.text):
        wallet = db.get_wallet(message.from_user.id)
        await message.delete()
        await async_bot.send_message(message.from_user.id,
            """Ваше Имя: <b>{}</b>\n-----------------------------\nВаш ID: <b>{}</b>\n-----------------------------\nВаш баланс: <b>{}р</b>""".format(
                message.from_user.username, message.from_user.id, wallet), reply_markup=top_up_markup)


@asbot.message_handler(Text(equals="Помощь"))
async def for_help(message: Message):
    if not is_number(message.text):
        await message.delete()
        await message.answer("За помощью пишите в лс:\n@VV50scheme\n@VV50scheme\n@VV50scheme", reply_markup=main_markup)


@asbot.message_handler(Text(equals="В начало"))
async def main_nav(message: Message):
    if not is_number(message.text):
        await message.answer("Выберите что-нибудь", reply_markup=main_markup)


@asbot.message_handler()
async def handle_amount(message: Message):
    if is_number(message.text):
        if int(message.text) >= 5:
            money = int(message.text)
            comment = str(message.chat.id) + "_" + str(randint(1000, 9999))
            bill = QIWI.bill(amount=money, lifetime=10, comment=comment)
            # db.top_up_wallet(cur_wallet=db.get_wallet(message.from_user.id), user_id=message.from_user.id, payment_amount=int(message.text))
            # await async_bot.send_message(message.from_user.id, "Вы пополнили баланс на {}р, и теперь он равен: {}".format(message.text, db.get_wallet(message.from_user.id)))
        else:
            await message.reply("Минимальная сумма для пополнения: 5р")
    else:
        await message.reply("Введите целое число ")


@asbot.callback_query_handler(text="top_up")
async def top_up(callback: CallbackQuery):
    await async_bot.delete_message(callback.from_user.id, callback.message.message_id)
    await async_bot.send_message(callback.message.chat.id, "Введите суумму для пополнения:", reply_markup=to_home_markup)


@asbot.callback_query_handler(text="to_main")
async def to_main(callback: CallbackQuery):
    await main_nav(message=callback.message)


if __name__ == '__main__':
    executor.start_polling(asbot, skip_updates=True)