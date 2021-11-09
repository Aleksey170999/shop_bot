import psycopg2
from asycnconf import USER, PASSWORD, HOST, DB_NAME


class Database:
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.USER = "postgres"
        self.PASSWORD = "Dmesggrepeth1"
        self.DB_NAME = "el_shopbot"

        self.connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DB_NAME)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT user_name FROM profile WHERE user_id ='{}'".format(user_id))
            result = self.cursor.fetchall()
            return bool(len(result))

    def create_user(self, user_id, user_name, wallet):
        with self.connection:
            self.cursor.execute("INSERT INTO profile(user_id, user_name, wallet) VALUES({}, '{}', {})".format(user_id, user_name, wallet))

    def get_wallet(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT wallet FROM profile WHERE user_id ='{}'".format(user_id))
            return int(self.cursor.fetchone()[0])

    def top_up_wallet(self, cur_wallet, user_id, payment_amount):
        with self.connection:
            self.cursor.execute("UPDATE profile SET wallet = {} WHERE user_id = '{}'".format(payment_amount + cur_wallet, user_id))


db = Database()
