import telebot
from telebot import types
import os

from telebot.types import Message

from text_file import bad_joke
import random as r
from database import Queue
from keyboard import *
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
queue = Queue()


def delete_first(message: Message) -> None:
    """
    Delete a first person in the queue
    """
    user = message.from_user.first_name
    if queue.queue_length():
        queue.delete_first_user()
        bot.send_message(message.chat.id, f"{user} был удален",
                         reply_markup=keyboard_admin)
        bot.send_message(queue.show_first_user()[3],
                         'Сейчас твоя очередь!')
        if queue.queue_length() > 1:
            bot.send_message(queue.show_all_user()[1][3],
                             "Приготовься, ты следуюющий)")
    else:
        bot.send_message(message.chat.id, "Некого удалять",
                         reply_markup=keyboard_admin)
    bot.register_next_step_handler(message, main)


def clear_queue(message: Message) -> None:
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


def get_in_line(message: Message) -> None:
    """
    Get to the end of the queue
    """
    if message.from_user.id not in \
            [user[3] for user in queue.show_all_user()]:
        bot.send_message(message.chat.id, 'Ваше имя и фамилия')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, "Ты уже в очереди!",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, send_welcome)


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


def view_queue(message: Message) -> None:
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


def back_to_main(message: Message) -> None:
    """
    Return to main menu
    """
    bot.send_message(message.chat.id, '/start', reply_markup=keyboard)
    bot.register_next_step_handler(message, send_welcome)


@bot.message_handler(commands=['start', 'admin'])
def start_message(message):
    if message.text == '/start':
        if admin(message):
            bot.send_message(message.chat.id, "Здравствуйте, мой господин", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Приветствую /start", reply_markup=keyboard)
    elif message.text == "/admin":
        bot.send_message(message.chat.id, "Введите пароль")
        bot.register_next_step_handler(message, get_password)


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    text = message.text.lower()
    if text in ['привет', 'здравствуй', "ку", "хей", "добрый день"]:
        bot.send_message(message.chat.id, "Привет, {}!".format(message.from_user.first_name))
    if text in ["я люблю тебя", 'я тебя люблю']:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMdXmBBaatmD8bUmYh_wvvCMQS5rKwAAg8AA0LhehVsOkNFYep6sxgE')
    if text == "расскажи шутку":
        bot.send_message(message.chat.id, bad_joke())
    # if text == "что нового?":
        # bot.send_message(message.chat.id, queue.show_all_user())
        # bot.send_message(message.chat.id, "[Новости мира видеоигр]({})".format(news()), parse_mode="Markdown")
    if text == "очередь":
        if admin(message):
            bot.send_message(message.chat.id, f"Что хотите сделать, {message.from_user.first_name}?", reply_markup=keyboard_admin)
            bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Вы хотите посмотреть или стать в очередь?", reply_markup=keyboard2)
            bot.register_next_step_handler(message, main)
    if text == "назад":
        bot.send_message(message.chat.id, '/start', reply_markup=keyboard)
        bot.register_next_step_handler(message, send_welcome)


# def queue_func(message):
#     text = message.text.lower()
#     if text == "удалить первого" and admin(message):
#         if queue.len_queue():
#             queue.delete_first_user()
#             bot.send_message(message.chat.id, f"Человек был удален", reply_markup=keyboard_admin)
#             bot.register_next_step_handler(message, queue_func)
#             if queue.len_queue() > 0:
#                 bot.send_message(queue.show_first_user()[0][3], 'Сейчас твоя очередь!')
#                 if queue.len_queue() > 1:
#                     bot.send_message(queue.show_first_user()[1][3], "Приготовься, скоро твоя очередь)")
#         else:
#             bot.send_message(message.chat.id, "Некого удалять", reply_markup=keyboard_admin)
#             bot.register_next_step_handler(message, queue_func)
#
#     if text == "очистить очередь" and admin(message):
#         if queue.len_queue():
#             queue.clear_queue()
#             bot.send_message(message.chat.id, "Очередь очищена!", reply_markup=keyboard_admin)
#             bot.register_next_step_handler(message, queue_func)
#         else:
#             bot.send_message(message.chat.id, "В очереди никого нет")
#             bot.register_next_step_handler(message, queue_func)
#
#     if text == "стать в очередь":
#         if message.from_user.id not in [queue.show_all_user()[i][3] for i in range(queue.len_of_queue())]:
#             bot.send_message(message.chat.id, 'Ваше имя и фамилия')
#             bot.register_next_step_handler(message, get_name)  # like input("message") = what we want to send
#         # queue_start = куди послати
#         else:
#             bot.send_message(message.chat.id, "Ты уже в очереди!", reply_markup=keyboard)
#             bot.register_next_step_handler(message, send_welcome)
#
#     if text == "посмотреть":
#         if not queue.len_of_queue():
#             bot.send_message(message.chat.id, "В очереди никого нет")
#             bot.register_next_step_handler(message, queue_func)
#         else:
#             if queue.len_of_queue() > 4:
#                 list_queue = queue.show_first_user() + \
#                              [(". . .", ". . .", ". . .", ". . .")] + \
#                              queue.show_last_user()
#             else:
#                 list_queue = queue.show_all_user()
#             for user_id, fname, lname, telegram_id in list_queue:
#                 bot.send_message(message.chat.id, f"{user_id} {fname} {lname}")
#             bot.register_next_step_handler(message, queue_func)
#
#     if text == "назад":
#         bot.send_message(message.chat.id, '/start', reply_markup=keyboard)
#         bot.register_next_step_handler(message, send_welcome)
def main(message: Message) -> None:
    """
    The main function of queue
    """
    text = message.text.lower()
    if text == "удалить первого":
        delete_first(message)
    if text == "очистить очередь":
        clear_queue(message)
    if text == "стать в очередь":
        get_in_line(message)
    if text == "посмотреть":
        view_queue(message)
    if text == "назад":
        back_to_main(message)


def get_name(message):  # получаем фамилию
    name = []
    name += message.text.split()
    if message.text.lower() == "назад":
        bot.send_message(message.chat.id, '/start', reply_markup=keyboard)
        bot.register_next_step_handler(message, send_welcome)
    elif len(name) == 1:
        bot.send_message(message.chat.id, "Нужно ввести полностью ИМЯ и ФАМИЛИЮ")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, "Тебя зовут {} {}?".format(name[0], name[1]), reply_markup=keyboard1)
        bot.register_next_step_handler(message, yesno, name[0], name[1])

# for i in range(3):
#     queue.add_user(f'last_name{i}', f'first_name{i}', i)

def yesno(message, *arg):
    text = message.text.lower()
    fname, lname = arg
    if text == 'да':
        queue.add_user(lname, fname, message.from_user.id)
        bot.send_message(message.chat.id, 'Запомню)', reply_markup=keyboard)
        bot.register_next_step_handler(message, send_welcome)
    elif text == "нет":
        bot.send_message(message.chat.id, 'Введи еще раз имя и фамилию')
        bot.register_next_step_handler(message, get_name)
    elif text == "*сарказм*":
        sarcasm = ['Ты что, не знаешь значения "Да" или "Нет"?', 'Маразм',
                   "'Колобок повесился' - а что ты ожидал увидеть?"]
        bot.send_message(message.chat.id, sarcasm[r.randint(0, 2)])
        bot.register_next_step_handler(message, get_name)
    if text == "назад":
        bot.send_message(message.chat.id, '/start', reply_markup=keyboard)
        bot.register_next_step_handler(message, send_welcome)


def admin(message):
    return message.from_user.id in [queue.show_admins()[i][1] for i in range(len(queue.show_admins()))]


def get_password(message):
    if message.text == "1604YAR":
        queue.add_admin(message.from_user.id)
        bot.send_message(message.chat.id, "Права администратора предоставлены", reply_markup=keyboard_admin)
        bot.register_next_step_handler(message, main)
    else:
        bot.send_message(message.chat.id, "Пароль введен неверно", reply_markup=keyboard)
        bot.register_next_step_handler(message, send_welcome)


bot.polling()
