import pymysql as pq
from pymysql.cursors import DictCursor
import contextlib as ctl


class BotQueue:
    def __init__(self):
        self.conn = pq.connect("localhost", 'root',
                               'agent0071604YAR00', 'bot_queue',
                               cursorclass=DictCursor)

    def insert(self, fname, lname):
        with ctl.closing(self.conn) as connection:
            query = "insert into bqueue(fname, lname, date_reg) values(%s, %s, current_time())"
            connection.cursor().execute(query, (fname, lname))
            connection.commit()

    def delete(self, user_id):
        with ctl.closing(self.conn) as connection:
            query = "delete from bqueue where user_id={}"
            connection.cursor().execute(query.format(user_id))
            connection.commit()

    def show_all(self):
        with ctl.closing(self.conn) as connection:
            with connection.cursor() as cursor:
                query = "select * from bqueue"
                cursor.execute(query)
                result = cursor.fetchall()
        return result

    def show_last(self):
        with ctl.closing(self.conn) as connection:
            with connection.cursor() as cursor:
                query = "select * from bqueue where user_id = (select max(user_id) from bqueue)"
                cursor.execute(query)
                result = cursor.fetchall()
        return result[0]

