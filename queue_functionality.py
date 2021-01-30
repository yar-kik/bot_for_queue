from telebot.types import Message

from database import Queue
from first_bot import bot, send_welcome, get_name
from keyboard import keyboard_admin, keyboard

queue = Queue()


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


def delete_first(message: Message) -> None:
    """
    Delete a first person in the queue
    """
    user = message.from_user.first_name
    if queue.len_of_queue():
        queue.delete_first_user()
        bot.send_message(message.chat.id, f"{user} был удален",
                         reply_markup=keyboard_admin)
        bot.send_message(queue.show_first_user()[3],
                         'Сейчас твоя очередь!')
        if queue.len_of_queue() > 1:
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
    if queue.len_of_queue():
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
            [telegram_id[3] for telegram_id in queue.show_all_user()]:
        bot.send_message(message.chat.id, 'Ваше имя и фамилия')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, "Ты уже в очереди!",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, send_welcome)


def view_queue(message: Message) -> None:
    """
    Function to see who is in line
    """
    if not queue.len_of_queue():
        bot.send_message(message.chat.id, "В очереди никого нет")
    else:
        if queue.len_of_queue() > 4:
            bot.send_message(message.chat.id, queue.show_first_user())
            bot.send_message(message.chat.id, (". . .", ". . .", ". . .", ". . ."))
            bot.send_message(message.chat.id, queue.show_last_user())
        else:
            for user_id, first_name, last_name, _ in queue.show_all_user():
                bot.send_message(message.chat.id, f"{first_name} {last_name}")
    bot.register_next_step_handler(message, main)


def back_to_main(message: Message) -> None:
    """
    Return to main menu
    """
    bot.send_message(message.chat.id, '/start', reply_markup=keyboard)
    bot.register_next_step_handler(message, send_welcome)
