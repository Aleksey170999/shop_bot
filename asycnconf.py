from aiogram import Bot, Dispatcher, types
from SimpleQIWI import *
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from pyqiwip2p import QiwiP2P


QIWI_TOKEN = "81a24bc005bb44a588131ed0e7aa907a"
PHONE = "+79506927724"
QIWI = QiwiP2P(auth_key=QIWI_TOKEN)

BOT_TOKEN = "2098590577:AAFEUxwx8sVzpcuAImg8IjH4HoxUlC0Ax7g"
async_bot = Bot(token=BOT_TOKEN,parse_mode=types.ParseMode.HTML)
asbot = Dispatcher(bot=async_bot)

HOST = "127.0.0.1"
USER = "postgres"
PASSWORD = "Dmesggrepeth1"
DB_NAME = "el_shopbot"

connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DB_NAME)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()


scheme = """
Нам нужно: 
 1. свежезареганный аккаунт, номера для регистрации берем на sms-activate.ru
 2. 10 минут вашего времени

Доставка осуществляется в два захода: первый вы делаете за деньги, второй - за возвращенные вам,  с первого заказа, баллы.
 3. Приступим. Для начала заходим в приложение  и набираем корзину на  1000+ рублей, это нужно, чтобы можно было ввести промокод, который дает скидку 200р, если чек 1000+.
 4. Оплачиваем 800р (1000 - 200) и ждем курьера
 5. Как только заказ в приложении будет считаться завершенным, заходим в него и нажимаем ‘Оформить возврат’
 6. Выбираем все товары, кроме пакета и в причине ставим ‘не понравился вкус’  или ‘истек срок годности’ на каждом товаре
 7. Подтверждаем возврат и ждем 3-5 минут, пока бот не начислит вам баллы( кстати, вернут вам не 800р, которые вы потратили, а 1000)
 8. Далее, снова набираем корзину на ту сумму, на которую вам начислили баллов и делаем еще 1 заказ, оплачивая его баллами полностью, ну или же доплатите какие-то копейки
 9. Ждем курьера второй раз
 10. Важно делать второй заказ как можно быстрее, потому что вкусвилл может аннулировать у вас рефнутые баллы, желательно в течении часа"""