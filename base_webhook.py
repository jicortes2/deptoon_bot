from flask import Flask, request
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space
from os import environ
from time import sleep
from random import choice
from constants import dawg_list, TOKEN, URL
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


"""
$ python3.5 flask_counter.py <token> <listening_port> <webhook_url>
Webhook path is '/abc', therefore:
<webhook_url>: https://<base>/abc
"""

PORT = int(environ.get("PORT", 5000))


class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            return

        text = msg['text']
        if text.startswith('/start'):
            bot.sendMessage(chat_id, 'Deptoon_bot is ready to begin')

        elif text.lower().startswith('/chaqueteardawg'):
            bot.sendMessage(chat_id, choice(dawg_list))
            # self.sender.sendMessage(self._count) no sirve para grupos

        elif text.startswith("/addchaqueteo"):
            text = text.replace("/addchaqueteo", "").lstrip()
            dawg_list.append(text)
            answer = "'{}' fue agregado al chaqueteo del dawg".format(text)
            bot.sendMessage(chat_id, answer)

        elif text.startswith("/listadawg"):
            answer = "** Chaqueteando al Dawg **\n\n"
            for i, phrase in enumerate(dawg_list):
                answer += "{}.- {}\n".format(i+1, phrase)
            bot.sendMessage(chat_id, answer, parse_mode="markdown")

        elif text.startswith("/deletechaqueteo"):
            text = text.replace("/deletechaqueteo", "").lstrip()
            try:
                answer = "'{}' fue eliminado de la lista de chaqueteo del dawg".format(dawg_list[int(text)-1])
                del dawg_list[int(text) - 1]
            except ValueError:
                answer = "El valor enviado no es un indice valido, prueba llamando a /listadawg para obtener el valor que buscas"
            except IndexError:
                answer = "El valor enviado no pertenece a la lista de chaqueteo del dawg, prueba llamando a /listadawg para obtener el valor que buscas"
            finally:
                bot.sendMessage(chat_id, answer)

        else:
            pass


app = Flask(__name__)
update_queue = Queue()  # channel between `app` and `bot`

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])
bot.message_loop(source=update_queue)  # take updates from queue


@app.route("/{}".format(TOKEN), methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'


if __name__ == '__main__':
    bot.setWebhook()
    sleep(1)
    bot.setWebhook(URL)
    app.run(host="0.0.0.0", port=PORT, debug=True)
