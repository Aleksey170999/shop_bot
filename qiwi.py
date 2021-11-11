from some_funcs import is_number
from markup import buy_menu
from db import db
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from random import randint
from pyqiwip2p import QiwiP2P


QIWI_TOKEN = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjgxZHY0ay0wMCIsInVzZXJfaWQiOiI3OTUwNjkyNzcyNCIsInNlY3JldCI6ImFhMGJmMWY3YzkzYTVlMzM1YTNjMTFkZjJmNWUzOTViYjAwMTg5YTc4NzdhMzg1NGZkZmU5ZGE2N2U4NmZjMWYifX0="
PHONE = "+79506927724"
QIWI = QiwiP2P(auth_key=QIWI_TOKEN)


# @dp.message_handler()
async def handle_amount(message: Message):
    if is_number(message.text):
        if int(message.text) >= 1:
            money = int(message.text)
            comment = str(message.chat.id) + "_" + str(randint(1000, 9999))

            bill = QIWI.bill(amount=money, lifetime=10, comment=comment)
            db.add_payment(message.from_user.id, money, bill.bill_id)

            await message.answer(
                "Вам нужно отправить <b>{}</b>р\nНа наш киви: <b>{}</b>\nС комментарием: <b>{}</b>".format(money, PHONE, comment),
                reply_markup=buy_menu(url=bill.pay_url, bill=bill.bill_id))
        else:
            await message.reply("Минимальная сумма для пополнения: 5р")
    else:
        await message.reply("Введите целое число ")


def register_handler_QIWI(dp: Dispatcher):
    dp.register_message_handler(handle_amount)