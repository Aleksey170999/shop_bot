from aiogram.types import *


to_home_markup = ReplyKeyboardMarkup(row_width=1).add(KeyboardButton("В начало"))

pay_balance_markup = ReplyKeyboardMarkup(row_width=1).add(
    KeyboardButton("Пополнить баланс"), KeyboardButton("В начало"))

main_markup = ReplyKeyboardMarkup(row_width=3).add(KeyboardButton('Категории',),
                                                                           KeyboardButton('Профиль'),
                                                                           KeyboardButton('Помощь'))

VV_50_markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text="Схема Вкусвилл за 40%", callback_data="VV_scheme"), InlineKeyboardButton(text="В начало", callback_data="to_main"))

top_up_markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Пополнить счёт", callback_data="top_up"), InlineKeyboardButton(text="В начало", callback_data="to_main"))


def buy_menu(isUrl=True, url="", bill=""):
    qiwi_menu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btn_url_qiwi = InlineKeyboardButton(text="Ссылка на оплату", url=url)
        qiwi_menu.insert(btn_url_qiwi)
    btn_check_qiwi = InlineKeyboardButton(text="Проверить оплату", callback_data="check_"+bill)
    qiwi_menu.insert(btn_check_qiwi)

    return qiwi_menu
