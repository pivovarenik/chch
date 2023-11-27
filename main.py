from regToQueue import *

surname = ' '


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "on_record":
        register_to_queue(call)

    elif call.data == "on_delete":
        print('тут егор работает')
    else:
        print('тут даша работает')


bot.polling(none_stop=True, interval=0)