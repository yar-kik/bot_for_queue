import telebot
import os

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(592676481, message.text)
bot.polling()