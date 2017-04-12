import telepot
import db
from bs4 import BeautifulSoup
import requests
from time import sleep
from random import choice
from telepot.delegate import per_chat_id, create_open, pave_event_space
from constants import TOKEN, deptoon_user
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


class Deptoon(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Deptoon, self).__init__(*args, **kwargs)

    def new_phrase(self, command, chat_id, id_sender):
        """ Agrega una frase para chaquetear al dawg """
        new_phrase = command.replace("/addchaqueteo", "").lstrip()
        if new_phrase.replace(" ", "") == "" or new_phrase == "@deptoon_bot":
            return "No puedes agregar '{}' al chaqueteo del dawg"
        elif id_sender == deptoon_user["dawg"]:
            return "{} fue agregado al chaqueteo del dawg... Jajaja claro que si, zoquete". format(new_phrase)
        db.add_element('dawg_list', chat_id, new_phrase)
        return "'{}' fue agregado al chaqueteo del dawg".format(new_phrase)

    def get_phrases(self, chat_id):
        """ Listado de frases para molestar al dawg """
        result = "** Chaqueteando al Dawg **\n\n"
        phrases = db.get_elements('dawg_list', chat_id)
        for i, phrase in enumerate(phrases):
            result += "{}.- {}\n".format(i+1, phrase)
        return result

    def get_phrase(self, chat_id):
        """ Retorna una frase para molestar al dawg """
        datos = db.get_elements('dawg_list', chat_id)
        return choice(datos)

    def delete_phrase(self, command, chat_id, id_sender):
        """ Elimina una frase del listado para chaquetear al dawg """
        if id_sender == deptoon_user["dawg"]:
            return "Buen intento dawg, pero tu chaqueteo se queda"
        index = command.replace("/deletechaqueteo", "").lstrip()
        phrases = db.get_elements('dawg_list', chat_id)
        for i, phrase in enumerate(phrases):
            if str(i+1) == str(index):
                db.delete_tuple('dawg_list', chat_id, phrase)
                return "{} - fue eliminada".format(phrase)
        return "No se encontro la frase"

    def add_products(self, command, chat_id):
        """ Agrega productos al carrito de supermercado """
        products = command.replace("/add", "").lstrip().split(',')
        if len(products[0]) == 0:
            return "Debes ingresar los productos asi: /add prod1, prod2, ..."
        else:
            for product in products:
                if len(product.lstrip()) > 0:
                    db.add_element('shop', chat_id, product.lstrip())
            if len(products) == 1:
                return "Se agregó 1 producto al carrito"
            else:
                return "Se agregaron {} productos al carrito".format(len(products))

    def clear_supermarket(self, chat_id):
        """ Vacia el carrito de supermercado """
        db.clear_table('shop', chat_id)
        return "Gracias por su compra, espero que no hayas olvidado nada!"

    def supermarket_list(self, chat_id):
        """ Listado de elementos en el carrito """
        result = "CARRITO DE SUPERMERCADO\n\n"
        products = db.get_elements('shop', chat_id)
        for prod in products:
            result += "- {}\n".format(prod)
        return result

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

    def papajohns(self, chat_id):
        base_url = "http://www.papajohns.cl"
        content = requests.get(base_url+'/pages/oclanding')
        soup = BeautifulSoup(content.text, 'html.parser')
        # print(soup)
        promo = soup.find("ul", {"id": "carousel_ul"})
        for img in promo:
            if img.find('img') != -1:
                image = base_url + img.find('img')['src'][2:]
                BOT.sendMessage(chat_id, image)
                sleep(2)





    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        user_id = msg["from"]["id"]
        if content_type != "text":
            return

        text = msg['text']
        answer = ""
        if text.startswith('/start'):
            answer = "Yow yow aqui deptoon_bot listo para zorronear"

        elif text.lower().startswith('/chaqueteardawg'):
            answer = self.get_phrase(chat_id)

        elif text.startswith("/addchaqueteo"):
            answer = self.new_phrase(text, chat_id, user_id)

        elif text.startswith("/listadawg"):
            answer = self.get_phrases(chat_id)
        # TODO: create db delete tuple
        elif text.startswith("/deletechaqueteo"):
            answer = self.delete_phrase(text, chat_id, user_id)

        elif text.startswith("/add"):
            answer = self.add_products(text, chat_id)

        elif text.startswith("/clear"):
            answer = self.clear_supermarket(chat_id)

        elif text.startswith("/supermercado"):
            answer = self.supermarket_list(chat_id)

        elif text.startswith("/getid"):
            answer = "Mensaje enviado por {}".format(str(user_id))

        elif text.startswith("/yowyow"):
            answer = self.yow_yow(user_id, chat_id)
            return

        elif text.startswith("/papajohns"):
            self.papajohns(chat_id)
            return

        BOT.sendMessage(chat_id, answer, parse_mode="Markdown")


UPDATE_QUEUE = Queue()  # channel between `app` and `bot`

BOT = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Deptoon, timeout=10),
])
BOT.message_loop(source=UPDATE_QUEUE)  # take updates from queue
