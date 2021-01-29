from telebot.types import Message

from database2 import Queue
from first_bot import bot
from keyboard import keyboard_admin, keyboard

queue = Queue()


def delete_first(message: Message) -> None:
    """
    Delete a first person in the queue
    """
    user = message.from_user.first_name
    if queue.len_queue():
        queue.delete_first_user()
        bot.send_message(message.chat.id, f"{user} был удален",
                         reply_markup=keyboard_admin)
        # bot.register_next_step_handler(message, queue_func)
        if queue.len_queue() > 0:
            bot.send_message(queue.show_first_user()[0][3], 'Сейчас твоя очередь!')
            if queue.len_queue() > 1:
                bot.send_message(queue.show_first_user()[1][3], "Приготовься, скоро твоя очередь)")
    else:
        bot.send_message(message.chat.id, "Некого удалять", reply_markup=keyboard_admin)
        # bot.register_next_step_handler(message, queue_func)


def clean_queue(message: Message) -> None:
    """
    Remove all people from the queue
    """
    if queue.len_queue():
        queue.clear_queue()
        bot.send_message(message.chat.id, "Очередь очищена!", reply_markup=keyboard_admin)
        # bot.register_next_step_handler(message, queue_func)
    else:
        bot.send_message(message.chat.id, "В очереди никого нет")
        # bot.register_next_step_handler(message, queue_func)


def get_in_line(message: Message) -> None:
    """
    Get to the end of the queue
    """
    if message.from_user.id not in [queue.show_all()[i][3] for i in range(queue.len_queue())]:
        bot.send_message(message.chat.id, 'Ваше имя и фамилия')
        # bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, "Ты уже в очереди!", reply_markup=keyboard)
        # bot.register_next_step_handler(message, send_welcome)


def view_queue(message: Message) -> None:
    """
    Function to see who is in line
    """
    if not queue.len_queue():
        bot.send_message(message.chat.id, "В очереди никого нет")
        # bot.register_next_step_handler(message, queue_func)
    else:
        if queue.len_queue() > 4:
            list_queue = queue.show_first_user() + \
                         [(". . .", ". . .", ". . .", ". . .")] + \
                         queue.show_last()
        else:
            list_queue = queue.show_all()
        for user_id, fname, lname, telegram_id in list_queue:
            bot.send_message(message.chat.id, f"{user_id} {fname} {lname}")
        # bot.register_next_step_handler(message, queue_func)