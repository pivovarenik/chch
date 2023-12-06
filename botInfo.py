import telebot
from telebot import types
import sqlite3
from sqlite3 import Error
import random
import time

bot = telebot.TeleBot('6708440193:AAHwhUWSbhwvtKwnU6kHkM8cpNEGfjoyvSQ')
randomed_dict = dict()

# здесь обрабатывается /start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        connection = sqlite3.connect(r"QueueDatabase.db")
    except Error as e:
        bot.send_message(message.from_user.id, 'Невозможно подключиться к БД, пните разрабов')
        return
    
    
    result = connection.execute(f'select ID from UserTable where ID = { message.from_user.id };')
    connection.close

    if (result.fetchall().__len__() != 0): # if user with this id already exists 
        bot.send_message(message.from_user.id, "Вы уже зареганы!")
        return
    bot.send_message(message.from_user.id, "Введите свою фамилию")
    bot.register_next_step_handler(message, get_surname) #следующий шаг – функция get_surname


@bot.message_handler(commands=['menu'])
def main_menu(message):
    try:
        connection = sqlite3.connect(r"QueueDatabase.db")
    except Error as e:
        bot.send_message(message.from_user.id, 'Невозможно подключиться к БД, пните разрабов')
        return
    
    result = connection.execute(f'select ID from UserTable where ID = { message.from_user.id };')
    connection.close

    if (result.fetchall().__len__() == 0): # if user with this id doesnt exist 
        start(message) # redirect to (main) menu
        return
    menu(message)


@bot.message_handler(commands=['help'])
def help_func(call):
    bot.send_message(call.chat.id, 
                     """Что я могу:
/help - выведется это сообщение
/start - только, чтобы зарегаться
/menu - перейти в главное меню
                     """)


def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Записаться на сдачу')
    item2 = types.KeyboardButton('Удалиться из очереди')
    item3 = types.KeyboardButton('Вывести список очереди')

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, '<pre>Hello! And welcome to the Los Pollos Hermanos family!\nMy name is Gustavo but u can call me SuS\nWhat do u want?</pre>', parse_mode='html', reply_markup=markup)
    
    # keyboard = types.InlineKeyboardMarkup(); #наша клавиатура

    # on_record_key = types.InlineKeyboardButton(text='Записаться на сдачу', callback_data='on_record') #кнопка
    # keyboard.add(on_record_key) #добавляем кнопку в клавиатуру

    # on_delete_key= types.InlineKeyboardButton(text='Удалиться из очереди', callback_data='on_delete')
    # keyboard.add(on_delete_key)

    # on_output_key= types.InlineKeyboardButton(text='Вывести список очереди', callback_data='on_output')
    # keyboard.add(on_output_key)

    # question = 'Вот что вы можете делать со мной:'
    # bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

def get_surname(message):
    surname = message.text

    try:
        connection = sqlite3.connect(r"QueueDatabase.db")
        connection.execute(f"""
            insert into UserTable(ID, Surname)
            values({ message.from_user.id }, '{surname}');
        """)
        connection.commit()
        connection.close
    except Error as e:
        bot.send_message(message.from_user.id, 'Невозможно подключиться к БД, пните разрабов')
        return

    bot.send_message(message.from_user.id, "Вы успешно зарегестрированы!")
