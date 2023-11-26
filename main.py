import telebot
from telebot import types
import sqlite3
from sqlite3 import Error
from regToQueue import *

bot = telebot.TeleBot('6708440193:AAHwhUWSbhwvtKwnU6kHkM8cpNEGfjoyvSQ')

surname = ' '

# здесь обрабатывается любой текст, который введет юзер
@bot.message_handler(content_types=['text'])
def start(message):
    text = message.text

    try:
        connection = sqlite3.connect(r"QueueDatabase.db")
    except Error as e:
        bot.send_message(message.from_user.id, 'Невозможно подключиться к БД, пните разрабов')
        return
        
    
    result = connection.execute(f'select ID from UserTable where ID = { message.from_user.id };')
    connection.close

    if result.fetchall().__len__() != 0 and text == '/start': # if user with this id already exists 
        bot.send_message(message.from_user.id, "Вы уже зарегестрированы!")
        menu(message) # redirect to (main) menu
    elif text == '/start':
        bot.send_message(message.from_user.id, "Введите свою фамилию")
        bot.register_next_step_handler(message, get_surname) #следующий шаг – функция get_surname
    else:
        bot.send_message(message.from_user.id, 'Не пон 🤨')


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


def menu(message):
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура

    on_record_key = types.InlineKeyboardButton(text='Записаться на сдачу', callback_data='on_record') #кнопка
    keyboard.add(on_record_key) #добавляем кнопку в клавиатуру

    on_delete_key= types.InlineKeyboardButton(text='Удалиться из очереди', callback_data='on_delete')
    keyboard.add(on_delete_key)

    on_output_key= types.InlineKeyboardButton(text='Вывести список очереди', callback_data='on_output')
    keyboard.add(on_output_key)

    question = 'Вот что вы можете делать со мной:'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "on_record":
        register_to_queue(call)

    elif call.data == "on_delete":
        print('тут егор работает')
    else:
        print('тут даша работает')


bot.polling(none_stop=True, interval=0)