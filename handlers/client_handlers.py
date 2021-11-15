from aiogram.dispatcher.filters import Text
from some_funcs import is_number
from create_bot import async_bot
from markups.client_markups import VV_50_markup, top_up_markup, to_home_markup, main_markup, buy_menu
from db import db
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import Dispatcher
from qiwi import QIWI
from stickers import jopik_fun


# @dp.message_handler(commands=['start'])
async def register(message: Message):
    if not is_number(message.text):
        if message.chat.type == "private":
            if not db.user_exists(message.from_user.id):
                db.create_user(message.from_user.id, message.from_user.username, wallet=0)
                await message.reply("Добро пожаловать, вы успешно зарегистрировались в боте.")
            await message.reply("Выберите что-нибудь", reply_markup=main_markup)


# @dp.message_handler(Text(equals="Категории"))
async def categories(message: Message):
    if not is_number(message.text):
        await message.delete()
        await async_bot.send_message(message.from_user.id, "Категории:", reply_markup=VV_50_markup)


# @dp.message_handler(Text(equals="Профиль"))
async def profile(message: Message):
    if not is_number(message.text):
        wallet = db.get_wallet(message.from_user.id)
        await message.delete()
        await async_bot.send_message(message.from_user.id,
                                     """Ваше Имя: <b>{}</b>\n-----------------------------\nВаш ID: <b>{}</b>\n-----------------------------\nВаш баланс: <b>{}р</b>""".format(
                                         message.from_user.username, message.from_user.id, wallet),
                                     reply_markup=top_up_markup)


# @dp.message_handler(Text(equals="Помощь"))
async def for_help(message: Message):
    if not is_number(message.text):
        await message.delete()
        await message.answer("За помощью пишите в лс:\n@VV50scheme\n@VV50scheme\n@VV50scheme", reply_markup=main_markup)


# @dp.message_handler(Text(equals="В начало"))
async def main_nav(message: Message):
    if not is_number(message.text):
        await message.delete()
        await message.answer("Выберите что-нибудь", reply_markup=main_markup)


# @dp.callback_query_handler(text_contains="check_")
async def check_payment(callback: CallbackQuery):
    bill = str(callback.data[6:])
    info = db.get_payment(bill)
    print(str(QIWI.check(bill_id=bill).status))
    if info:
        if str(QIWI.check(bill_id=bill).status) == "PAID":

            money = db.get_money(bill)
            current_wallet = db.get_wallet(callback.from_user.id)
            db.top_up_wallet(current_wallet, callback.from_user.id, money)
            db.delete_payment(bill)
            await async_bot.send_message(callback.from_user.id, "Вы пополнили баланс на {}р, и теперь он равен: {}".format(money, current_wallet+money))
            db.delete_payment(bill)
        else:
            await callback.message.answer("Вы не оплатили счёт", reply_markup=buy_menu(False, bill=bill))


# # @dp.callback_query_handler(text="top_up")
# async def top_up(callback: CallbackQuery):
#     await async_bot.delete_message(callback.from_user.id, callback.message.message_id)
#     await async_bot.send_message(callback.message.chat.id, "Введите суумму для пополнения:",
#                                  reply_markup=to_home_markup)


# @dp.callback_query_handler(text="to_main")
async def to_main(callback: CallbackQuery):
    await main_nav(message=callback.message)


# @dp.callback_query_handler(text="VV_scheme")
async def buy_scheme(callback: CallbackQuery):
    cur_wallet = db.get_wallet(callback.from_user.id)
    if cur_wallet >= 5000:
        db.top_up_wallet(cur_wallet, callback.from_user.id, -5000)
        await callback.message.delete()
        await callback.message.answer_sticker(jopik_fun)
    else:
        await callback.message.answer("Недостаточно деняк.", reply_markup=top_up_markup)


def register_client_message_handlers(dp: Dispatcher):
    dp.register_message_handler(categories, Text(equals="Категории"))
    dp.register_message_handler(profile, Text(equals="Профиль"))
    dp.register_message_handler(for_help, Text(equals="Помощь"))
    dp.register_message_handler(main_nav, Text(equals="В начало"))
    dp.register_message_handler(register, commands=['start'])


def register_client_query_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(check_payment, text_contains="check_")
    # dp.register_callback_query_handler(top_up, text_contains="top_up")
    dp.register_callback_query_handler(to_main, text_contains="to_main")
    dp.register_callback_query_handler(buy_scheme, text_contains="VV_scheme")
