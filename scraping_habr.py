from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
import sqlite3


def table_exists(db_name: str, table_name: str) -> bool:
    """
    Check if table exist in database
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' "
                   f"AND name='{table_name}'")
    exist = bool(cursor.fetchone()[0])
    connection.close()
    return exist


def create_table(db_name: str, table_name: str) -> None:
    """
    Function to create table and (if not exists) database
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} "
                   "(article_id INTEGER PRIMARY KEY, "
                   "url TEXT, "
                   "title TEXT);")
    connection.commit()
    connection.close()


def save_data(db_name: str, table_name: str, data: List[tuple]) -> None:
    """
    Function to save data to database table
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    if not table_exists(db_name, table_name):
        create_table(db_name, table_name)
    cursor.executemany(f"INSERT INTO {table_name} (url, title)"
                       f" VALUES(?, ?);", data)
    connection.commit()
    connection.close()


def get_articles(db_name: str, table_name: str, count: int = None) -> List[
    Tuple]:
    """
    Function to get data from database table
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    if not table_exists(db_name, table_name):
        create_table(db_name, table_name)
    if count is None:
        cursor.execute(f'SELECT * FROM {table_name} ')
    else:
        cursor.execute(f'SELECT * FROM {table_name} '
                       f'ORDER BY article_id ASC LIMIT {count}')
    return cursor.fetchall()


def parse_article_from_site(url: str) -> list:
    """
    Parse site and return tuple with article url, title, text and tags
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.find_all('article', class_='post post_preview')
    new_articles = []
    for article_data in articles:
        title_with_link = article_data.find('a', class_='post__title_link')
        title = title_with_link.text
        article_url = title_with_link['href']
        if article_url not in [article[1] for article in
                               get_articles('habr.db', 'habr_db')]:
            article = (article_url, title)
            new_articles.append(article)
    return new_articles


def add_new_articles(db_name: str, table_name: str, url: str) -> None:
    """
    Add parsed article to database
    """
    save_data(db_name, table_name, parse_article_from_site(url))
