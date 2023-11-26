from botInfo import *

def register_to_queue(call):
    bot.send_message(call.message.chat.id, 'Выберите предмет:')

    try:
        connection = sqlite3.connect(r"QueueDatabase.db")
    except Error as e:
        bot.send_message(call.message.chat.id, 'Невозможно подключиться к БД, пните разрабов')
        return

    result = connection.execute(f'select * from LabTable;')
    labs_list = result.fetchall()


    subject_info = """
| ID | Название предмета | Подгруппа |
===================================
"""

    for i in range(len(labs_list)):
        subject_info += f"| {labs_list[i][0]: <{3}}"
        subject_info += f"| {labs_list[i][1]: <{30}}|"
        subject_info += f" {labs_list[i][2]: ^{10}}|\n"
        #print(subject_info)
    bot.send_message(call.message.chat.id, subject_info)
