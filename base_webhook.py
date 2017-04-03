import telepot
from flask import Flask, request
# import os
from itertools import cycle
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


TOKEN = '318756416:AAHSgDPf-XJWUuImHoEKoJqvWAZf2TSqQgU'
# HTOKEN = os.environ(TOKEN)
app = Flask(__name__)
SECRET = "/bot{}".format(TOKEN)
URL = "https://stark-tor-45686.herokuapp.com/"
BOT = telepot.Bot(TOKEN)
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
    print("entra")
    if text.lower().startswith('/chaqueteardawg'):
        answer = dawg_list
    else:
        answer = "Yow yow"
    BOT.sendMessage(chat_id, "{}".format(answer))

BOT.message_loop({'chat': on_chat_message}, source=UPDATE_QUEUE)


@app.route(SECRET, methods=['GET', 'POST'])
def pass_update():
    UPDATE_QUEUE.put(request.data)
    return 'OK'

BOT.setWebhook(URL + SECRET)
app.run(host='0.0.0.0', port=8080, debug=False)