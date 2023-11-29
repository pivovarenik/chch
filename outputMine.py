from deleteFromQueue import *


def display_queue(call):
    try:
        connection = sqlite3.connect(r"QueueDatabase.db")
    except Error as e:
        bot.send_message(call.message.chat.id, 'Невозможно подключиться к БД, пните разрабов')
        return
    
    record_data = connection.execute(f'select * from Record;')
    records_list = record_data.fetchall()

    if len(records_list) == 0:
        bot.send_message(call.message.chat.id, "Никто не хочет сдавать лабы(\nСписок пустой")
        return

    labs_data = connection.execute(f'select * from LabTable;')
    labs_list = labs_data.fetchall()

    for lab in labs_list:
        current_time = (int)(time.strftime("%H%M", time.localtime()))

        current_users_lab_count = connection.execute(f'select * from Record where LabID = {lab[0]}').fetchall()

        if (int)(lab[4].replace(':', '')) > current_time:
            text = f'Запись для\n{lab[1]}---Группа: {lab[2]}---{lab[3]}\nеще не окончена\n\nСейчас записано: {len(current_users_lab_count)} чел.'
            bot.send_message(call.message.chat.id, text)
            continue

        dictionary_key = lab[1] + (str)(lab[2]) # lab name and group number is a key

        global randomed_dict
        try:
            randomed_dict[dictionary_key]
            pass
        except:
            users_data = connection.execute(f'''select UserTable.Surname, Record.LabsCount, LabTable.LabName, LabTable.GroupNumber 
                                                from Record 
                                                join Labtable on Record.LabID = Labtable.ID
                                                join UserTable on Record.UserID = UserTable.ID
                                                Where  Labtable.ID = {lab[0]};''')
            randomed_dict[dictionary_key] = users_data.fetchall()

            random.shuffle(randomed_dict[dictionary_key])

        show_randomed_users_queue(call, randomed_dict[dictionary_key])
    
    connection.close()


def show_randomed_users_queue(call, queue):
    users_queue = """| № | Фамилия              | Кол-во лаб | Название лабы | Подгруппа
=======================================================
"""

    for counter in range(len(queue)):
        users_queue += f"| {(str)(counter + 1):^{4}}" # place
        users_queue += f"| {queue[counter][0]: ^{17}}" # name
        users_queue += f"| {queue[counter][1]: <{20}}" # labs count
        users_queue += f"| {queue[counter][2]: <{20}}" # subject
        users_queue += f"| {queue[counter][3]: ^{15}}\n" if (str)(queue[counter][1]).__len__() == 1 else  f"| {queue[counter][1]: ^{16}}\n" # group
    bot.send_message(call.message.chat.id, users_queue)
