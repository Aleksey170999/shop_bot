from some_funcs import is_number
from markups.client_markups import buy_menu
from db import db
from aiogram.types import *
from aiogram.dispatcher import Dispatcher
from random import randint
from pyqiwip2p import QiwiP2P
from create_bot import dp, async_bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from markups.client_markups import *
from markups.admin_markups import *

QIWI_TOKEN = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjgxZHY0ay0wMCIsInVzZXJfaWQiOiI3OTUwNjkyNzcyNCIsInNlY3JldCI6ImFhMGJmMWY3YzkzYTVlMzM1YTNjMTFkZjJmNWUzOTViYjAwMTg5YTc4NzdhMzg1NGZkZmU5ZGE2N2U4NmZjMWYifX0="
PHONE = "+79506927724"
QIWI = QiwiP2P(auth_key=QIWI_TOKEN)


class FSMPayment(StatesGroup):
    count_to_pay = State()


@dp.callback_query_handler(text="top_up", state=None)
async def top_up(callback: CallbackQuery):
    await FSMPayment.count_to_pay.set()
    await callback.message.answer("Введите суумму для пополнения:", reply_markup=cancel)


@dp.message_handler(content_types=['text'], state=FSMPayment.count_to_pay)
async def handle_amount(message: Message, state: FSMContext):
    if is_number(message.text):
        if int(message.text) >= 1:
            comment = str(message.chat.id) + "_" + str(randint(1000, 9999))
            async with state.proxy() as data:
                data['amount'] = int(message.text)
                bill = QIWI.bill(amount=data['amount'], lifetime=10, comment=comment)
                db.add_payment(message.from_user.id, data['amount'], bill.bill_id)
            await state.finish()
            await message.answer(
                "Вам нужно отправить <b>{}</b>р\nНа наш киви: <b>{}</b>\nС комментарием: <b>{}</b>".format(data['amount'], PHONE,
                                                                                                           comment),
                reply_markup=buy_menu(url=bill.pay_url, bill=bill.bill_id))
        else:
            await message.reply("Минимальная сумма для пополнения: 5р")
    else:
        await message.reply("Введите целое число ")


@dp.callback_query_handler(text="cancel_payment", state="*")
async def cancel_payment(callback: CallbackQuery, state: FSMContext):
    bill = db.get_bill_id(callback.from_user.id)
    db.delete_payment(bill)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.delete()
    await callback.message.answer("Отмена!")


@dp.callback_query_handler(text="cancel_2")
async def cancel_payment(callback: CallbackQuery):
    bill = db.get_bill_id(callback.from_user.id)
    db.delete_payment(bill)
    await callback.message.answer("Отмена2!!!")


def register_handler_QIWI(dp: Dispatcher):
    dp.register_message_handler(handle_amount, content_types=['text'], state=FSMPayment.count_to_pay)
    dp.register_callback_query_handler(top_up, text="top_up", state=None)

