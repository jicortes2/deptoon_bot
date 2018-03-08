"""Deptoon_bot main handler"""
from time import sleep
from bs4 import BeautifulSoup
import requests
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space
# from telepot.loop import MessageLoop
from constants import TOKEN, deptoon_user, BOT_NAME, LOCAL_TEST, TEST_TOKEN
from telegram_handler import TelegramHandler as TH
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


def parse_command(command):
    command = command.replace("@{}".format(BOT_NAME), "")
    return getattr(TH, command, TH.default)


class Deptoon(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Deptoon, self).__init__(*args, **kwargs)

    def papajohns(self, *args):
        """ Scraping a la pagina de papa johns que envia las imagenes del
        carousel del inicio, en caso de que la página cambie es necesario
        actualizar """
        chat_id = args
        base_url = "http://www.papajohns.cl"
        content = requests.get(base_url+'/pages/oclanding')
        soup = BeautifulSoup(content.text, 'html.parser')
        promo = soup.find("ul", {"id": "carousel_ul"})
        for img in promo:
            if img.find('img') != -1:
                image = base_url + img.find('img')['src'][2:]
                BOT.sendMessage(chat_id, image)
                sleep(2)

    def yow_yow(self, id_sender, chat_id):
        """ Send yow yow sticker depending of the user """
        if id_sender == deptoon_user["cris"]:  # Cristian
            id_sticker = "CAADAQADDAADDNuWDOx7HiPygX7BAg"
        elif id_sender == deptoon_user["juan"]:  # Juan
            id_sticker = "CAADAQADCAADDNuWDHREnLw8FWs0Ag"
        elif id_sender == deptoon_user["cati"]:  # Cati
            id_sticker = "CAADAQADTQADDNuWDMI0-pPy7z-7Ag"
        elif id_sender == deptoon_user["dawg"]:  # Dawg
            id_sticker = "CAADAQADBgADDNuWDKuOezm3e36nAg"
        elif id_sender == deptoon_user["rocio"]:  # Rocio
            id_sticker = "CAADAgADSAEAAhhC7giR8ls8wm-QoQI"
        elif id_sender == deptoon_user["belen"]:  # Tor
            id_sticker = "CAADAgADQwEAAvR7GQABHefwRWSx0_IC"
        else:
            id_sticker = "CAADBAADUQEAAtoAAQ4JYteU7EX3eYgC"
        BOT.sendSticker(chat_id, sticker=id_sticker)

    def find_message_type(self, msg, chat_id):
        if msg.get("document", False):
            BOT.sendMessage(chat_id, "entro a document")
            gif_id = msg["document"]["file_id"]
            BOT.sendMessage(chat_id, str(gif_id))
            sleep(1)
        elif msg.get("video", False):
            BOT.sendMessage(chat_id, "entro a video")
            gif_id = msg["video"]["file_id"]
            BOT.sendMessage(chat_id, str(gif_id))
            sleep(1)
        elif msg.get("sticker", False):
            BOT.sendMessage(chat_id, "entro a sticker")
            gif_id = msg["sticker"]["file_id"]
            BOT.sendMessage(chat_id, str(gif_id))
            sleep(1)
        elif msg.get("photo", False):
            BOT.sendMessage(chat_id, "entro a photo")
            gif_id = msg["photo"]["file_id"]
            BOT.sendMessage(chat_id, str(gif_id))
            sleep(1)
        elif msg.get("audio", False):
            BOT.sendMessage(chat_id, "entro a audio")
            gif_id = msg["video"]["file_id"]
            BOT.sendMessage(chat_id, str(gif_id))
            sleep(1)

    def final_day(self, chat_id):
        BOT.sendSticker(chat_id, sticker="CAADBAAD5gADydJaAAES6wuk1Er55wI")
        sleep(2)
        answer = "Llegó el día... no podemos evitar lo inevitable..."
        BOT.sendMessage(chat_id, answer, parse_mode="Markdown")
        sleep(3)
        # Homero
        BOT.sendDocument(chat_id, document="CgADBAADnw4AAq0bZAebvzwdpMqs3AI")
        sleep(3)
        answer = "Pero no todo esta perdido..."
        BOT.sendMessage(chat_id, answer, parse_mode="Markdown")
        sleep(2)
        end_aragorn = "https://www.youtube.com/watch?v=ApUu1DA5HCs"
        BOT.sendMessage(chat_id, end_aragorn, parse_mode="html")

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        user_id = msg["from"]["id"]

        if False:
            # Cambiar para debuggear o saber el type de algo
            # Recuerda cambiar el setting de privacy mode
            self.find_message_type(msg, chat_id)

        text = msg['text']
        answer = ""

        if text.startswith("/yowyow") or text.lower() == "yow yow":
            self.yow_yow(user_id, chat_id)
            return

        elif text.startswith("/papajohns"):
            self.papajohns(chat_id)
            return

        elif text.startswith("/thefinalday"):
            self.final_day(chat_id)
            return

        elif text.startswith("/"):
            command = text.split(" ")[0].replace("/", "")
            command = parse_command(command)
            answer = command(text, chat_id, user_id)

        BOT.sendMessage(chat_id, answer, parse_mode="Markdown")


if LOCAL_TEST:
    # BOT = telepot.DelegatorBot(TEST_TOKEN, [
    #     pave_event_space()(
    #         per_chat_id(), create_open, Deptoon, timeout=10),
    #     ])
    # MessageLoop(BOT).run_as_thread()
    while 1:
        sleep(10)
else:
    UPDATE_QUEUE = Queue()  # channel between `app` and `bot`

    BOT = telepot.DelegatorBot(TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, Deptoon, timeout=10),
    ])
    BOT.message_loop(source=UPDATE_QUEUE)  # take updates from queue
