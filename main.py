from outputQueue import *

surname = ' '


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "on_record":
        register_to_queue(call)
    elif call.data == "on_delete":
        delete_from_queue(call)
    else:
        DisplayQueue(call.message)


bot.polling(none_stop=True, interval=0)