import sqlite3 as pq


class BotQueue:
    def __init__(self):
        self.conn = pq.connect(':memory:', check_same_thread=False)
        self.conn.execute("create table if not exists bqueue "
                          "(user_id integer primary key, fname text, lname text, "
                          "telegram_id integer)")
        self.conn.execute("create table if not exists administrators "
                          "(user_id integer primary key, telegram_id integer)")

    def admin_granted(self, telegram_id):
        connection = self.conn
        query = "insert into administrators(telegram_id) values(?)"
        connection.cursor().execute(query, (telegram_id,))
        connection.commit()

    def show_admin(self):
        cursor = self.conn.cursor()
        query = "select * from administrators"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def insert(self, fname, lname, telegram_id):
        connection = self.conn
        query = "insert into bqueue(fname, lname, telegram_id) values(?, ?, ?)"
        connection.cursor().execute(query, (fname, lname, telegram_id))
        connection.commit()

    def delete_first(self):
        connection = self.conn
        #query = "delete from bqueue order by user_id asc limit 1"
        query = "DELETE FROM bqueue WHERE user_id BETWEEN (SELECT MIN(user_id) FROM bqueue) " \
                "AND (SELECT MIN(user_id) FROM bqueue)"
        connection.cursor().execute(query)
        connection.commit()

    def reset(self):
        connection = self.conn
        query = "delete from bqueue"
        connection.cursor().execute(query)
        connection.commit()

    def show_first(self):
        cursor = self.conn.cursor()
        #query = "select * from bqueue order by user_id asc limit 2"
        query = "select * from bqueue where user_id between (select min(user_id) from bqueue) " \
                "and (select min(user_id) from bqueue)+1"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def show_last(self):
        cursor = self.conn.cursor()
        # query = "select * from bqueue order by user_id desc limit 2"
        query = "select * from bqueue where user_id between (select max(user_id) from bqueue)-1 " \
                "and (select max(user_id) from bqueue)"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def show_all(self):
        cursor = self.conn.cursor()
        query = "select * from bqueue"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def len_queue(self):
        cursor = self.conn.cursor()
        query = "select count(*) from bqueue"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]
