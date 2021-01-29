import sqlite3
from typing import *


class Queue:
    """
    Class to interact with sqlite database
    """

    def __init__(self, queue_db: str = 'bot_queue',
                 admins_db: str = 'admins') -> None:
        """
        Create databases for a queue and admins of the queue
        :queue_db: The name of a created queue database.
        :admins_db: The name of a created admins database.
        """
        self._queue_db = queue_db
        self._admins_db = admins_db
        self._connection = sqlite3.connect(':memory:',
                                           check_same_thread=False)
        self.cursor = self._connection.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {queue_db} "
                            "(user_id INTEGER PRIMARY KEY, "
                            "first_name TEXT, "
                            "last_name TEXT, "
                            "telegram_id INTEGER);")
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {admins_db} "
                            "(user_id INTEGER PRIMARY KEY, "
                            "telegram_id INTEGER);")
        self._connection.commit()

    def create_admin(self, telegram_id: Union[int, str]) -> None:
        """
        Add new admin to database
        """
        self.cursor.execute(f"INSERT INTO {self._admins_db} "
                            f"(telegram_id) VALUES(?);", (telegram_id,))
        self._connection.commit()

    def show_admins(self) -> List[Tuple]:
        """
        Show all admins
        """
        self.cursor.execute(f"SELECT * FROM {self._admins_db};")
        admins = self.cursor.fetchall()
        return admins

    def add_user(self, first_name: str, last_name: str,
                 telegram_id: Union[str, int]) -> None:
        """
        Add a new user to database
        """
        self.cursor.execute(f"INSERT INTO {self._queue_db} "
                            f"(first_name, last_name, telegram_id) "
                            f"VALUES (?, ?, ?);",
                            (first_name, last_name, telegram_id))
        self._connection.commit()

    def delete_first_user(self) -> None:
        """
        Delete first row of queue database table
        """
        self.cursor.execute(f"DELETE FROM {self._queue_db} WHERE user_id IN "
                            f"(SELECT user_id FROM {self._queue_db} "
                            f"ORDER BY user_id ASC LIMIT 1)")
        self._connection.commit()

    def clear_queue(self) -> None:
        """
        Delete all users from queue
        """
        self.cursor.execute(f"DELETE FROM {self._queue_db}")
        self._connection.commit()

    def show_first_user(self) -> Tuple[int, str]:
        """
        Return first user of the queue
        """
        self.cursor.execute(f"SELECT * FROM {self._queue_db} "
                            f"ORDER BY user_id ASC LIMIT 1")
        first_user = self.cursor.fetchone()
        return first_user

    def show_last(self) -> Tuple[int, str]:
        """
        Return last user of the queue
        """
        self.cursor.execute(f"SELECT * FROM {self._queue_db} "
                            f"ORDER BY user_id ASC LIMIT 1")
        last_user = self.cursor.fetchone()
        return last_user

    def show_all(self):
        cursor = self.connection.cursor()
        query = "select * from bqueue"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def len_queue(self):
        cursor = self.connection.cursor()
        query = "select count(*) from bqueue"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]
