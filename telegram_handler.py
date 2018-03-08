"""Class to manage deptoon_bot telegram commands"""
from random import choice
from constants import deptoon_user
import db


class TelegramHandler:
    """
    new_phrase(frase) - agrega la frase para chaquetear al dawg
    chaqueteandawg - retorna la lista de chaqueteando al dawg
    chaquetear - retorna una frase al azar de la lista del dawg
    add(p1, p2, p3...) - recibe productos separados por ',' y los agrega al carrito
    clear_list - vacia el carrito de supermercado
    supermarket_list - retorna la lista del supermercado"""
    @staticmethod
    def start():
        """Deptoon_bot starting method"""
        return "Yow yow aqui deptoon_bot listo para zorronear"

    @staticmethod
    def new_phrase(*args):
        """ Agrega una frase para chaquetear al dawg """
        command, chat_id, id_sender = args
        new_phrase = command.replace("/addchaqueteo", "").lstrip()
        if new_phrase.replace(" ", "") == "" or new_phrase == "@deptoon_bot":
            return "No puedes agregar '{}' al chaqueteo del dawg"
        elif id_sender == deptoon_user["dawg"]:
            return "{} fue agregado al chaqueteo del dawg... Jajaja claro"\
                   " que si, zoquete". format(new_phrase)
        db.add_element('dawg_list', chat_id, new_phrase)
        return "'{}' fue agregado al chaqueteo del dawg".format(new_phrase)

    @staticmethod
    def chaqueteandawg(*args):
        """ Listado de frases para molestar al dawg """
        command, chat_id, id_sender = args
        result = "** Chaqueteando al Dawg **\n\n"
        phrases = db.get_elements('dawg_list', chat_id)
        for i, phrase in enumerate(phrases):
            result += "{}.- {}\n".format(i+1, phrase)
        return result

    @staticmethod
    def chaquetear(*args):
        """ Retorna una frase para molestar al dawg """
        command, chat_id, id_sender = args
        datos = db.get_elements('dawg_list', chat_id)
        return choice(datos)

    @staticmethod
    def delete_phrase(*args):
        """ Elimina una frase del listado para chaquetear al dawg """
        command, chat_id, id_sender = args
        if id_sender == deptoon_user["dawg"]:
            return "Buen intento dawg, pero tu chaqueteo se queda"
        index = command.replace("/deletechaqueteo", "").lstrip()
        phrases = db.get_elements('dawg_list', chat_id)
        for i, phrase in enumerate(phrases):
            if str(i+1) == str(index):
                db.delete_tuple('dawg_list', chat_id, phrase)
                return "{} - fue eliminada".format(phrase)
        return "No se encontro la frase"

    @staticmethod
    def add(*args):
        """ Agrega productos al carrito de supermercado """
        command, chat_id, id_sender = args
        products = command.replace("/add", "").lstrip().split(',')
        if len(products[0]) == 0:
            return "Debes ingresar los productos asi: /add prod1, prod2, ..."
        else:
            for product in products:
                if len(product.lstrip()) > 0:
                    db.add_element('shop', chat_id, product.lstrip())
            if len(products) == 1:
                return "Se agregó 1 producto al carrito"
            return "Se agregaron {} productos al carrito".format(len(products))

    @staticmethod
    def clear_list(*args):
        """ Vacia el carrito de supermercado """
        command, chat_id, id_sender = args
        db.clear_table('shop', chat_id)
        return "Gracias por su compra, espero que no hayas olvidado nada!"

    @staticmethod
    def supermarket_list(*args):
        """ Listado de elementos en el carrito """
        command, chat_id, id_sender = args
        result = "CARRITO DE SUPERMERCADO\n\n"
        products = db.get_elements('shop', chat_id)
        for prod in products:
            result += "- {}\n".format(prod)
        return result

    @staticmethod
    def default(*args):
        """ Default action in case of wrong method """
        return TelegramHandler.__doc__
