import os
from typing import List

from telebot.types import Message

from database import Queue
from keyboard import *
from scraping_habr import get_articles, add_new_articles

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
queue = Queue()
NAME_DB = 'habr.db'
ARTICLE_TABLE = 'habr_db'
NEWS_TABLE = 'news'
ARTICLE_URL = "https://habr.com/ru/all/"
NEWS_URL = 'https://habr.com/ru/news/'


def main(message: Message) -> None:
    """
    The main function of queue
    """
    text = message.text.lower()
    if text == "удалить первого" and is_admin(message):
        delete_first(queue, message)
    if text == "очистить очередь" and is_admin(message):
        clear_queue(queue, message)
    if text == "стать в очередь":
        get_in_line(queue, message)
    if text == "посмотреть":
        view_queue(queue, message)
    if text == "назад":
        back_to_main(message)


def delete_first(queue: Queue, message: Message) -> None:
    """
    Delete a first person in the queue
    """
    if queue.queue_length():
        deleted_user = queue.delete_first_user()
        first_name, last_name = deleted_user[1], deleted_user[2]
        bot.send_message(message.chat.id,
                         f"\"{first_name} {last_name}\" был удален",
                         reply_markup=keyboard_admin)
        if queue.queue_length() > 0:
            bot.send_message(queue.show_first_user()[3],
                             'Сейчас твоя очередь!')
        if queue.queue_length() > 1:
            bot.send_message(queue.show_all_user()[1][3],
                             "Приготовься, ты следуюющий)")
    else:
        bot.send_message(message.chat.id, "Некого удалять",
                         reply_markup=keyboard_admin)
    bot.register_next_step_handler(message, main)


def clear_queue(queue: Queue, message: Message) -> None:
    """
    Remove all people from the queue
    """
    if queue.queue_length():
        queue.clear_queue()
        bot.send_message(message.chat.id, "Очередь очищена!",
                         reply_markup=keyboard_admin)
    else:
        bot.send_message(message.chat.id, "В очереди никого нет")
    bot.register_next_step_handler(message, main)


def get_in_line(queue: Queue, message: Message) -> None:
    """
    Get to the end of the queue
    """
    if message.from_user.id not in \
            [telegram_id[3] for telegram_id in queue.show_all_user()]:
        bot.send_message(message.chat.id, 'Ваше имя и фамилия')
        bot.register_next_step_handler(message, get_full_name)
    else:
        bot.send_message(message.chat.id, "Ты уже в очереди!",
                         reply_markup=keyboard_main)
        bot.register_next_step_handler(message, main_menu)


def view_queue(queue: Queue, message: Message) -> None:
    """
    Function to see who is in line
    """
    if not queue.queue_length():
        bot.send_message(message.chat.id, "В очереди никого нет")
    else:
        if queue.queue_length() > 4:
            bot.send_message(message.chat.id, show_many_users(queue))
        else:
            bot.send_message(message.chat.id, show_few_users(queue))
    bot.register_next_step_handler(message, main)


def show_many_users(queue: Queue) -> str:
    """
    Return string with first and last 2 users
    """
    users_list = ''
    for user_id, first_name, last_name, _ in queue.show_first_user(2):
        users_list += f"[{user_id}] {first_name} {last_name}\n"
    users_list += '. . . . . . . .\n'
    for user_id, first_name, last_name, _ in reversed(queue.show_last_user(2)):
        users_list += f"[{user_id}] {first_name} {last_name}\n"
    return users_list


def show_few_users(queue: Queue) -> str:
    """
    Return string with all users
    """
    users_list = ''
    for user_id, first_name, last_name, _ in queue.show_all_user():
        users_list += f"[{user_id}] {first_name} {last_name}\n"
    return users_list


def back_to_main(message: Message) -> None:
    """
    Return to main menu
    """
    bot.send_message(message.chat.id, '/start', reply_markup=keyboard_main)
    bot.register_next_step_handler(message, main_menu)


@bot.message_handler(commands=['admin'])
def get_admin_rights(message: Message) -> None:
    bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(message, get_password)
    if message.text == "назад":
        back_to_main(message)


@bot.message_handler(commands=['start'])
def start_message(message):
    if is_admin(message):
        bot.send_message(message.chat.id, "Здравствуйте, мой господин",
                         reply_markup=keyboard_main)
    else:
        bot.send_message(message.chat.id, "Приветствую /start",
                         reply_markup=keyboard_main)


def get_articles_title(articles: List[tuple]) -> str:
    """"""
    titles = [f"{i}. [{article[2]}]({article[1]})" for i, article
              in enumerate(articles, 1)]
    titles = '\n\n'.join(titles)
    return titles


def get_habr(message: Message) -> None:
    """"""
    text = message.text.lower()
    if text == "статьи":
        add_new_articles(NAME_DB, ARTICLE_TABLE, ARTICLE_URL)
        articles = get_articles(NAME_DB, ARTICLE_TABLE, 8)
        titles = get_articles_title(articles)
        bot.send_message(message.chat.id, titles,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, get_habr)
    if text == 'новости':
        add_new_articles(NAME_DB, NEWS_TABLE, NEWS_URL)
        articles = get_articles(NAME_DB, NEWS_TABLE, 8)
        titles = get_articles_title(articles)
        bot.send_message(message.chat.id, titles,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, get_habr)
    if text == "назад":
        back_to_main(message)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    text = message.text.lower()
    if text == "что нового?":
        bot.send_message(message.chat.id,
                         "Статьи или новости?", reply_markup=keyboard_habr)
        bot.register_next_step_handler(message, get_habr)
    if text == "очередь":
        if is_admin(message):
            bot.send_message(message.chat.id,
                             f"Что хотите сделать, "
                             f"{message.from_user.first_name}?",
                             reply_markup=keyboard_admin)
            bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id,
                             "Вы хотите посмотреть или стать в очередь?",
                             reply_markup=keyboard2)
            bot.register_next_step_handler(message, main)
    if text == "назад":
        back_to_main(message)


def get_full_name(message: Message) -> None:
    """
    Function to get full name of user
    """
    name = []
    name += message.text.split()
    if message.text.lower() == "назад":
        bot.send_message(message.chat.id, '/start', reply_markup=keyboard_main)
        bot.register_next_step_handler(message, main_menu)
    elif len(name) == 1:
        bot.send_message(message.chat.id,
                         "Нужно ввести полностью ИМЯ и ФАМИЛИЮ")
        bot.register_next_step_handler(message, get_full_name)
    else:
        bot.send_message(message.chat.id, f"Тебя зовут {name[0]} {name[1]}?",
                         reply_markup=keyboard1)
        bot.register_next_step_handler(message, get_answer, name[0], name[1])


def get_answer(message, *arg) -> None:
    """
    Confirm user input
    """
    text = message.text.lower()
    if text == 'да':
        queue.add_user(*arg, message.from_user.id)
        bot.send_message(message.chat.id, 'Запомню)', reply_markup=keyboard_main)
        bot.register_next_step_handler(message, main_menu)
    if text == "нет":
        bot.send_message(message.chat.id, 'Введи еще раз имя и фамилию')
        bot.register_next_step_handler(message, get_full_name)
    if text == "назад":
        back_to_main(message)


def is_admin(message: Message) -> bool:
    """
    Check if a user is an admin
    """
    return message.from_user.id in [admin[1] for admin in queue.show_admins()]


def get_password(message) -> None:
    """
    Get password to give admin rights
    """
    if message.text == "pass":
        queue.add_admin(message.from_user.id)
        bot.send_message(message.chat.id, "Права администратора предоставлены",
                         reply_markup=keyboard_admin)
        bot.register_next_step_handler(message, main)
    else:
        bot.send_message(message.chat.id, "Пароль введен неверно",
                         reply_markup=keyboard_main)
        bot.register_next_step_handler(message, main_menu)


bot.polling()
