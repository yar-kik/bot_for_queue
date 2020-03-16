import telebot
from telebot import types

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)  # виклик клавіатури. щоб була меншою і щоб ховалася
keyboard.row("Что нового?", "Расскажи шутку", "Очередь")

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row("Посмотреть", "Стать в очередь", "Назад")

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row("Да", "Нет", "Назад")

keyboard_admin = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_admin.row("Посмотреть", "Стать в очередь", "Назад")
keyboard_admin.row("Удалить первого", "Очистить очередь")
