import telepot
from random import choice
from telepot.delegate import per_chat_id, create_open, pave_event_space
from constants import TOKEN
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


class Deptoon(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Deptoon, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            return

        text = msg['text']
        answer = ""
        if text.startswith('/start'):
            answer = "Yow yow aqui deptoon_bot listo para zorronear"

        elif text.lower().startswith('/chaqueteardawg'):
            # Retorna una frase para molestar al dawg
            with open("db/dawg_list.txt") as file:
                datos = file.readlines()
            answer = choice(datos)

        elif text.startswith("/addchaqueteo"):
            # Agrega una frase para chaquetear al dawg
            text = text.replace("/addchaqueteo", "").lstrip()
            with open("db/dawg_list.txt", "a") as file:
                file.write("{}\n".format(text))
            answer = "'{}' fue agregado al chaqueteo del dawg".format(text)

        elif text.startswith("/listadawg"):
            # Listado de frases para molestar al dawg
            answer = "** Chaqueteando al Dawg **\n\n"
            with open("db/dawg_list.txt") as file:
                dawg_list = file.readlines()
                for i, phrase in enumerate(dawg_list):
                    answer += "{}.- {}".format(i+1, phrase)

        elif text.startswith("/deletechaqueteo"):
            # Elimina una frase del listado para chaquetear al dawg
            try:
                with open("db/dawg_list.txt") as file:
                    facts = file.readlines()

                text = int(text.replace("/deletechaqueteo", "").lstrip())
                if int(text) < 0:
                    answer = "'{}' fue eliminado de la lista de chaqueteo del dawg".format(
                        facts[text])
                    del facts[text]
                else:
                    answer = "'{}' fue eliminado de la lista de chaqueteo del dawg".format(
                        facts[text - 1])
                    del facts[text - 1]
                with open("db/dawg_list.txt", "w") as file:
                    for dato in facts:
                        file.write("{}".format(dato))

            except ValueError:
                answer = "El valor enviado no es un indice valido, prueba llamando a /listadawg para obtener el valor que buscas"
            except IndexError:
                answer = "El valor enviado no pertenece a la lista de chaqueteo del dawg, prueba llamando a /listadawg para obtener el valor que buscas"
        elif text.startswith("/add"):
            # Agrega productos al carrito de supermercado
            products = text.replace("/add", "").lstrip().split(',')
            with open("db/shop.txt", 'a') as f:
                for prod in products:
                    f.write("{}\n".format(prod))
            answer = "Se agregaron {} productos al carrito".format(len(products))
        elif text.startswith("/clear"):
            # Vacia el carrito de supermercado
            with open("db/shop.txt", 'w') as f:
                pass
            answer = "Gracias por su compra, espero que no hayas olvidado nada!"
        elif text.startswith("/supermercado"):
            # Listado de elementos en el carrito
            answer = "CARRITO DE SUPERMERCADO\n\n"
            with open("db/shop.txt", 'r') as f:
                for i, prod in enumerate(f):
                    answer += "{}. {}".format(i, prod)

        BOT.sendMessage(chat_id, answer, parse_mode="Markdown")


UPDATE_QUEUE = Queue()  # channel between `app` and `bot`

BOT = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Deptoon, timeout=10),
])
BOT.message_loop(source=UPDATE_QUEUE)  # take updates from queue
