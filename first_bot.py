import telebot
from telebot import types
from text_file import bad_joke
from whats_new import news

name = ''
surname = ''
age = 0

bot = telebot.TeleBot("926024610:AAHK2vj_OKHq5l4eKZnoWz9b3jWYqQVA-5Q")
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)  # виклик клавіатури. щоб була меншою і щоб ховалася
keyboard.row("Что нового?", "Расскажи шутку", "Стать в очередь")



@bot.message_handler(commands=['start'])  # бот реагує на "старт"
def start_message(message):
    bot.send_message(message.chat.id, "Приветствую /start", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    text = message.text.lower()
    if text in ['привет', 'здравствуй', "ку", "хей", "добрый день"]:
        bot.send_message(message.chat.id, " Привет, {}!".format(message.from_user.first_name))
    if text in ["я люблю тебя", 'я тебя люблю']:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMdXmBBaatmD8bUmYh_wvvCMQS5rKwAAg8AA0LhehVsOkNFYep6sxgE')
    if text == "расскажи шутку":
        bot.send_message(message.chat.id, bad_joke())
    if text == "что нового?":
        bot.send_message(message.chat.id, "[Новости мира видеоигр]({})".format(news()), parse_mode="Markdown")
    if text == "стать в очередь":
        bot.send_message(message.chat.id, 'Как тебя зовут?')
        bot.register_next_step_handler(message, get_name) #like input("message") = what we want to send
        #queue_start = куди послати

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row("Да","Нет","*Сарказм*")

def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.chat.id, "Имя {} введено верно?".format(message.text), reply_markup=keyboard1)
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Какая у тебя фамилия?')
        bot.register_next_step_handler(message, get_surname)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, 'Введи еще раз имя')
        bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.chat.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        ... #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню)')
    elif call.data == "no":
        bot.register_next_step_handler()




bot.polling()
