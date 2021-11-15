import logging
from aiogram import executor
from create_bot import dp
from handlers.client_handlers import register_client_message_handlers, register_client_query_handlers
from qiwi import register_handler_QIWI

logging.basicConfig(level=logging.INFO)  # Логгинг бота в консоль

register_client_message_handlers(dp)  # Регистрация хэндлеров сообщений  клиента

register_client_query_handlers(dp)  # Регистрация хэндлеров коллбэков  клиента

register_handler_QIWI(dp)  # Регистрация хэндлеров сообщений  клиента для оплаты QIWI


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
