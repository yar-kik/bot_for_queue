import pymysql as pq
from pymysql.cursors import DictCursor
import contextlib as ctl


class BotQueue:
    def __init__(self):
        self.conn = pq.connect("localhost", 'root',
                               'agent0071604YAR00', 'bot_queue',
                               cursorclass=DictCursor)

    def admin_granted(self, telegram_id):
        connection = self.conn
        query = "insert into administrators(telegram_id) values(%s)"
        connection.cursor().execute(query, telegram_id)
        connection.commit()

    def show_admin(self):
        connection = self.conn
        with connection.cursor() as cursor:
            query = "select * from administrators"
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def insert(self, fname, lname, telegram_id):
        connection = self.conn
        query = "insert into bqueue(fname, lname, date_reg, telegram_id) values(%s, %s, current_time(), %s)"
        connection.cursor().execute(query, (fname, lname, telegram_id))
        connection.commit()

    def delete_first(self):
        connection = self.conn
        #query = "delete from bqueue where user_id = (select min(user_id) from (select * from bqueue) as new_table)"
        query = "delete from bqueue order by user_id asc limit 1"
        connection.cursor().execute(query)
        connection.commit()

    def reset(self):
        connection = self.conn
        query = "truncate table bqueue"
        connection.cursor().execute(query)
        connection.commit()

    def show_first(self):
        connection = self.conn
        with connection.cursor() as cursor:
            query = "select * from bqueue where user_id between (select min(user_id) from bqueue) " \
                    "and (select min(user_id) from bqueue)+1"
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def show_last(self):
        connection = self.conn
        with connection.cursor() as cursor:
            query = "select * from bqueue where user_id between (select max(user_id) from bqueue)-1 " \
                    "and (select max(user_id) from bqueue)"
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def show_all(self):
        connection = self.conn
        with connection.cursor() as cursor:
            query = "select * from bqueue"
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def len_queue(self):
        connection = self.conn
        with connection.cursor() as cursor:
            query = "select count(*) from bqueue"
            cursor.execute(query)
            result = cursor.fetchone()
        return result['count(*)']

# d = BotQueue()
# print(d.len_queue())
