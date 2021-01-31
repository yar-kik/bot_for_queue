import telebot
from telebot import types

keyboard_main = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_main.row("Что нового?", "Очередь")

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row("Посмотреть", "Стать в очередь", "Назад")

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row("Да", "Нет", "Назад")

keyboard_habr = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_habr.row('Статьи', "Новости", "Назад")

keyboard_admin = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_admin.row("Посмотреть", "Стать в очередь", "Назад")
keyboard_admin.row("Удалить первого", "Очистить очередь")
