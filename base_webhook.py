from flask import Flask, request
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space
from os import environ
from time import sleep
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

"""
$ python3.5 flask_counter.py <token> <listening_port> <webhook_url>
Webhook path is '/abc', therefore:
<webhook_url>: https://<base>/abc
"""

class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        self._count += 1
        self.sender.sendMessage(self._count)


# deptoon_bot = "318756416:AAHSgDPf-XJWUuImHoEKoJqvWAZf2TSqQgU"
TOKEN = "361066388:AAH-TSjo2oz1XzDMCcRz_bRfW4KHej-M3so"
PORT = int(environ.get("PORT", 5000))
URL = "https://dry-mesa-62011.herokuapp.com/{}".format(TOKEN)

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