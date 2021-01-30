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
        self.__queue_db = queue_db
        self.__admins_db = admins_db
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

    @property
    def queue_db(self) -> str:
        """
        Return name of the queue database
        """
        return self.__queue_db

    @property
    def admins_db(self) -> str:
        """
        Return name of the queue database
        """
        return self.__admins_db

    def add_admin(self, telegram_id: Union[int, str]) -> None:
        """
        Add new admin to database
        """
        self.cursor.execute(f"INSERT INTO {self.admins_db} "
                            f"(telegram_id) VALUES(?);", (telegram_id,))
        self._connection.commit()

    def show_admins(self) -> List[Tuple]:
        """
        Show all admins
        """
        self.cursor.execute(f"SELECT * FROM {self.admins_db};")
        admins = self.cursor.fetchall()
        return admins

    def add_user(self, first_name: str, last_name: str,
                 telegram_id: Union[str, int]) -> None:
        """
        Add a new user to database
        """
        self.cursor.execute(f"INSERT INTO {self.queue_db} "
                            f"(first_name, last_name, telegram_id) "
                            f"VALUES (?, ?, ?);",
                            (first_name, last_name, telegram_id))
        self._connection.commit()

    def delete_first_user(self) -> None:
        """
        Delete first row of queue database table
        """
        self.cursor.execute(f"DELETE FROM {self.queue_db} WHERE user_id IN "
                            f"(SELECT user_id FROM {self.queue_db} "
                            f"ORDER BY user_id ASC LIMIT 1)")
        self._connection.commit()

    def clear_queue(self) -> None:
        """
        Delete all users from queue
        """
        self.cursor.execute(f"DELETE FROM {self.queue_db}")
        self._connection.commit()

    def show_first_user(self, n: int = 1) -> Union[Tuple, List[Tuple]]:
        """
        Return first user of the queue
        :n: Amount of the first users.
        """
        self.cursor.execute(f"SELECT * FROM {self.queue_db} "
                            f"ORDER BY user_id ASC LIMIT {n}")
        if n == 1:
            return self.cursor.fetchone()
        return self.cursor.fetchall()

    def show_last_user(self, n: int = 1) -> Union[Tuple, List[Tuple]]:
        """
        Return last user of the queue
        :n: Amount of the last users.
        """
        self.cursor.execute(f"SELECT * FROM {self.queue_db} "
                            f"ORDER BY user_id DESC LIMIT {n}")
        if n == 1:
            return self.cursor.fetchone()
        return self.cursor.fetchall()

    def show_all_user(self) -> List[Tuple]:
        """
        Return all user of the queue
        """
        self.cursor.execute(f"SELECT * FROM {self.queue_db}")
        users = self.cursor.fetchall()
        return users

    def queue_length(self) -> int:
        """
        Return the number of people in the queue
        """
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.queue_db}")
        result = self.cursor.fetchone()
        return result[0]
