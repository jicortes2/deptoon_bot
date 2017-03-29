import sys
from flask import Flask, request
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

"""
$ python3.5 flask_counter.py <token> <listening_port> <webhook_url>
Webhook path is '/abc', therefore:
<webhook_url>: https://<base>/abc
"""

TOKEN = '318756416:AAHSgDPf-XJWUuImHoEKoJqvWAZf2TSqQgU'
# HTOKEN = os.environ(TOKEN)
SECRET = "/bot{}".format(TOKEN)
URL = "https://api.telegram.org/"
PORT = 5000


class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        self._count += 1
        self.sender.sendMessage(self._count)


app = Flask(__name__)
update_queue = Queue()  # channel between `app` and `bot`

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])
bot.message_loop(source=update_queue)  # take updates from queue

@app.route('/abc', methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'

if __name__ == '__main__':
    bot.setWebhook(URL)
    app.run(port=PORT, debug=True)
"""import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space
from flask import Flask, request
# import os
# from itertools import cycle
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


TOKEN = '318756416:AAHSgDPf-XJWUuImHoEKoJqvWAZf2TSqQgU'
# HTOKEN = os.environ(TOKEN)
app = Flask(__name__)
SECRET = "/bot{}".format(TOKEN)
URL = "https://api.telegram.org/"
# BOT = telepot.Bot(TOKEN)
UPDATE_QUEUE = Queue()
dawg_list = cycle([
                    'Dawg acuerdate de comprar las tazas',
                    'Dawg, no te ibai en marzo?',
                    'Hace cuanto no vas al supermercado dawg?',
                    'Te acuerdas donde queda el super dawg?',
                    'Dawg compra pan'
                ])


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
                    return
                text = msg["text"]
                if text.lower().startswith('/chaqueteardawg'):
                    answer = dawg_list
                else:
                    answer = "Yow yow"
    BOT.sendMessage(chat_id, "{}".format(answer))


BOT.message_loop({'chat': on_chat_message}, source=UPDATE_QUEUE)
class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        self._count += 1
        self.sender.sendMessage(self._count)

@app.route(SECRET, methods=['GET', 'POST'])
def pass_update():
    UPDATE_QUEUE.put(request.data)
    return 'OK'


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])
bot.message_loop(source=UPDATE_QUEUE)


bot.setWebhook(URL + SECRET)
"""