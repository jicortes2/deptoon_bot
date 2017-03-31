import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space
from flask import Flask, request
# import os
# from itertools import cycle
try:
    from Queue import Queue
except ImportError:
    from queue import Queue
"""ON_HEROKU = os.environ.get('ON_HEROKU')

if ON_HEROKU:
    # get the heroku port
    PORT = int(os.environ.get('PORT', 17995))  # as per OP comments default is 17995
else:
    PORT = 3000
"""

TOKEN = '318756416:AAHSgDPf-XJWUuImHoEKoJqvWAZf2TSqQgU'
# HTOKEN = os.environ(TOKEN)
app = Flask(__name__)
SECRET = "/bot{}".format(TOKEN)
URL = "https://api.telegram.org/"
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

bot.setWebhook(URL + SECRET)
app.run(port=8080, debug=True)