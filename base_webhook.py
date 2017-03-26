import flask
import telepot
from os import environ
try:
	from Queue import Queue
except ImportError:
	from queue import Queue


BOT_TOKEN = '318756416:AAHSgDPf-XJWUuImHoEKoJqvWAZf2TSqQgU'
TOKEN = environ(BOT_TOKEN)
app = flask(__name__)
SECRET = "/bot{}".format(TOKEN)
URL = "	"
BOT = telepot.Bot(TOKEN)
UPDATE_QUEUE = Queue()


def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	BOT.sendMessage(chat_id, 'hello!')


BOT.message_loop({'chat': on_chat_message}, source=UPDATE_QUEUE)

@app.route(SECRET, methods=['GET', 'POST'])
def pass_update():
	UPDATE_QUEUE.put(request.data)
	return 'OK'


BOT.setWebhook(URL + SECRET)