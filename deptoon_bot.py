import telepot
from random import choice
from telepot.delegate import per_chat_id, create_open, pave_event_space
from constants import TOKEN
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

""" 255008894 - Cristian
    211213068 - Juan
    253564139 - Cati

    STICKERS
    DAWG = CAADAQADBgADDNuWDKuOezm3e36nAg"""


class Deptoon(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Deptoon, self).__init__(*args, **kwargs)

    def new_phrase(self, command):
        """ Agrega una frase para chaquetear al dawg """
        command = command.replace("/addchaqueteo", "").lstrip()
        with open("db/dawg_list.txt", "a") as file:
            file.write("{}\n".format(command))
        return "'{}' fue agregado al chaqueteo del dawg".format(command)

    def get_phrases(self):
        """ Listado de frases para molestar al dawg """
        phrases = "** Chaqueteando al Dawg **\n\n"
        with open("db/dawg_list.txt") as file:
            dawg_list = file.readlines()
            for i, phrase in enumerate(dawg_list):
                phrases += "{}.- {}".format(i+1, phrase)
        return phrases

    def get_phrase(self):
        """ Retorna una frase para molestar al dawg """
        with open("db/dawg_list.txt", "r") as f:
            datos = f.readlines()
        return choice(datos)

    def delete_phrase(self, command):
        """ Elimina una frase del listado para chaquetear al dawg """
        try:
            with open("db/dawg_list.txt") as file:
                facts = file.readlines()

            text = int(command.replace("/deletechaqueteo", "").lstrip())
            if int(text) < 0:
                answer = "'{}' fue eliminado de la lista de chaqueteo del dawg".format(
                    facts[text].replace('\n', ''))
                del facts[text]
            else:
                answer = "'{}' fue eliminado de la lista de chaqueteo del dawg".format(
                    facts[text - 1].replace('\n', ''))
                del facts[text - 1]
            with open("db/dawg_list.txt", "w") as file:
                for dato in facts:
                    file.write("{}".format(dato))
            return answer

        except ValueError:
            answer = "El valor enviado no es un indice valido, prueba llamando a /listadawg para obtener el valor que buscas"
        except IndexError:
            answer = "El valor enviado no pertenece a la lista de chaqueteo del dawg, prueba llamando a /listadawg para obtener el valor que buscas"

    def add_products(self, command):
        """ Agrega productos al carrito de supermercado """
        products = command.replace("/add", "").lstrip().split(',')
        if len(products[0]) == 0:
            return "Debes ingresar los productos asi: /add prod1, prod2, ..."
        else:
            with open("db/shop.txt", 'a') as f:
                for prod in products:
                    f.write("{}\n".format(prod.lstrip()))
            if len(products) == 1:
                return "Se agregó 1 producto al carrito"
            else:
                return "Se agregaron {} productos al carrito".format(len(products))

    def clear_supermarket(self):
        """ Vacia el carrito de supermercado """
        with open("db/shop.txt", 'w'):
            pass
        return "Gracias por su compra, espero que no hayas olvidado nada!"

    def supermarket_list(self):
        """ Listado de elementos en el carrito """
        products = "CARRITO DE SUPERMERCADO\n\n"
        with open("db/shop.txt", 'r') as f:
            for prod in f:
                products += "- {}".format(prod)
        return products

    def yow_yow(self, user_id, chat_id):
        if user_id == 255008894:  # Cristian
            id_sticker = "CAADAQADDAADDNuWDOx7HiPygX7BAg"
        elif user_id == 211213068:  # Juan
            id_sticker = "CAADAQADCAADDNuWDHREnLw8FWs0Ag"
        elif user_id == 253564139:  # Cati
            id_sticker = "CAADAQADTQADDNuWDMI0-pPy7z-7Ag"
        else:
            BOT.sendMessage(chat_id, "No tienes yow yow sticker :(")
        BOT.sendSticker(chat_id, sticker=id_sticker)

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
            answer = self.get_phrase()

        elif text.startswith("/addchaqueteo"):
            answer = self.new_phrase(text)

        elif text.startswith("/listadawg"):
            answer = self.get_phrases()

        elif text.startswith("/deletechaqueteo"):
            answer = self.delete_phrase(text)

        elif text.startswith("/add"):
            answer = self.add_products(text)

        elif text.startswith("/clear"):
            answer = self.clear_supermarket()

        elif text.startswith("/supermercado"):
            answer = self.supermarket_list()

        elif text.startswith("/getid"):
            answer = "Mensaje enviado por {}".format(str(user_id))

        elif text.startswith("yow yow"):
            self.yow_yow(user_id, chat_id)
            return

        BOT.sendMessage(chat_id, answer, parse_mode="Markdown")


UPDATE_QUEUE = Queue()  # channel between `app` and `bot`

BOT = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Deptoon, timeout=10),
])
BOT.message_loop(source=UPDATE_QUEUE)  # take updates from queue
