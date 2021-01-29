import unittest
from database2 import Queue


class TestQueue(unittest.TestCase):
    """
    Class to test interacting with database
    """
    def setUp(self) -> None:
        self.queue = Queue(queue_db='queue', admins_db='admins')

    def test_create_admin(self):
        self.queue.create_admin(1234)
        self.queue.cursor.execute("SELECT * FROM admins;")
        admin = self.queue.cursor.fetchone()
        self.assertIn(1234, admin)

    def test_show_admins(self):
        admins = self.queue.show_admins()
        self.assertEqual(admins, [])

        data = [(1, 1234), (2, 1235)]
        self.queue.cursor.executemany("INSERT INTO admins VALUES(?, ?);", data)
        admins = self.queue.show_admins()
        self.assertEqual(admins, data)

    def test_add_user(self):
        self.queue.add_user('foo', 'bar', 123)
        self.queue.cursor.execute("SELECT * FROM queue;")
        user = self.queue.cursor.fetchone()
        self.assertIn('foo', user)

    def test_delete_first_user(self):
        self.queue.cursor.executemany('INSERT INTO queue VALUES (?, ?, ? ,?);',
                                  [(1, 'foo', 'bar', 123),
                                   (2, 'bar', 'foo', 124)])
        self.queue.delete_first_user()
        self.queue.cursor.execute("SELECT * FROM queue;")
        user = self.queue.cursor.fetchone()
        self.assertEqual(user, (2, 'bar', 'foo', 124))

    def test_clear_queue(self):
        self.queue.cursor.executemany('INSERT INTO queue VALUES (?, ?, ? ,?);',
                                  [(1, 'foo', 'bar', 123),
                                   (2, 'bar', 'foo', 124)])
        self.queue.clear_queue()
        users = self.queue.cursor.fetchall()
        self.assertEqual(users, [])

    def test_show_first_user(self):
        self.queue.cursor.executemany('INSERT INTO queue VALUES (?, ?, ? ,?);',
                                  [(1, 'foo', 'bar', 123),
                                   (2, 'bar', 'foo', 124)])
        user = self.queue.show_first_user()
        self.assertEqual(user, (1, 'foo', 'bar', 123))
