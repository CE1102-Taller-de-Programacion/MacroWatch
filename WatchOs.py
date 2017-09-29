import json
import datetime
import random


class Persona:
    def __init__(self, identidad, nombre, telefonos, celular, correo, foto):
        self.identidad = identidad
        self.nombre = nombre
        self.telefonos = telefonos
        self.celular = celular
        self.correo = correo
        self.foto = foto


def confirma_pin(data):
    with open("config.json", "r") as f:
        config = json.load(fp=f)

    if data == config["pin"]:
        return True
    else:
        return False


class Contactos:
    """
        Maneja, muestra y administra los contactos del sistema.
    """
    def __init__(self):

        # Carga los contactos del disco.
        with open("contactos.json", "r") as f:
            self.contact = self.json.load(fp=f)

    def crear(self, identidad, nombre, telefonos, celular, correo, foto):
        """
        :param identidad:
        :param nombre:
        :param telefonos:
        :param celular:
        :param correo:
        :param foto:
        :return: bool que indica el éxito de agregar el contacto.

        Agrega un usuario a la lista de contactos
        """
        self.contact["ids"] += [identidad]
        self.contact["nombres"] += [nombre]
        self.contact["telefonos"] += [telefonos]
        self.contact["celular"] += [celular]
        self.contact["correos"] += [correo]
        self.contact["fotos"] += [foto]

    def eliminar(self, identidad):
        i = self.contact["ids"].index(identidad)
        self.contact["ids"][i] = None
        self.contact["nombres"] = None
        self.contact["telefonos"] = None
        self.contact["celular"] = None
        self.contact["correos"] = None
        self.contact["fotos"] = None

        self.sort(["ids", "nombres", "telefonos", "celular", "correos", "fotos"])

    def sort(self, keys):
        pass

    def ordenar(self, modo):
        """
        :param modo
        :return: result

        General un dict copia de contac, el cual se ordena con Selection Sort según el modo especificado.
        """
        result = self.contact
        if modo == "ID":
            for i in range(0, result["ids"]):
                menor = i
                for j in range(0, result["ids"]+1):
                    if result["ids"][j] < result["ids"][menor]:
                        menor = j
                result["ids"][i], result["ids"][menor] = result["ids"][menor], result["ids"][i]
                result["nombres"][i], result["nombres"][menor] = result["nombres"][menor], result["nombres"][i]
                result["telefonos"][i], result["telefonos"][menor] = result["telefonos"][menor], result["telefonos"][i]
                result["celular"][i], result["celular"][menor] = result["celular"][menor], result["celular"][i]
                result["correos"][i], result["correos"][menor] = result["correos"][menor], result["correos"][i]
                result["fotos"][i], result["fotos"][menor] = result["fotos"][menor], result["fotos"][i]

            return result
        """
        elif modo == "Alfabetico":
            for i in range(0, result[modo]):
                menor = i
                for j in range(0, result[modo]+1):
                    if result[modo][j] < result[modo][menor]:
                        menor = j
                result[modo][i], result[modo][menor] = result[modo][menor], result[modo][i]
        """
    def seleccionar(self, identidad):
        try:
            i = self.contact["ids"].index(identidad)
            return [self.contact["ids"][i], self.contact["nombres"][i], self.contact["telefonos"][i],
                    self.contact["celular"][i], self.contact["correos"][i], self.contact["fotos"[i]]]
        except IndexError:
            return False

    def save(self):
        try:
            with open("contactos.json", "w") as f:
                json.dump(obj=self.contact, fp=f)
            return True
        except FileNotFoundError:
            return False


class Calculadora:
    def suma(self, *args):
        pass

    def resta(self, *args):
        pass

    def producto(self, *args):
        pass

    def division(self, *args):
        pass


class Agenda:
    pass


class Ahorcado:
    """
    Clase que maneja la lógica para el juego de ahorcado
    Genera la palabra a utilizar y comprueba cada vez que se le pide
    """
    def __init__(self, idi):
        self.idi = idi

        with open("pal.json", "r") as f:
            load = json.load(fp=f)
        if self.idi:
            i = random.randint(0, len(load["palabras"]))
            self.actual = load["palabras"][i]
        else:
            i = random.randint(0, load["words"])
            self.actual = load["words"][i]

    def get_actual(self):
        return self.actual

    def comprobar_letra(self, letra):
        """
        :param letra: char
        :return: bool que indica si la letra dada por el usuario está en la
        palabra actual.
        """
        result = False
        if letra in self.actual:
            result = True
        return result

    # Hacer en shell para que no pueda enviar "palabra" vacío.
    def comprobar_palabra(self, palabra):
        """
        :param palabra: string array
        :return: bool que indica si el usuario a logrado adivinar todas las letras
        de la palabra actual.
        """
        temp = self.actual
        return self.comprobar_palabra_aux(palabra, temp)

    def comprobar_palabra_aux(self, palabra, temp):
        if palabra is None and temp is None:
            return True
        elif palabra[0] in temp:
            i = temp.index(palabra[0])
            self.comprobar_palabra_aux(palabra[1:], temp[:i])
        else:
            return False


def cambiar_pin(nuevo_pin):
    try:
        if isinstance(nuevo_pin, str) and 0 < int(nuevo_pin) <= 9999:
            with open("config.json", "r") as f:
                temp = json.load(fp=f)
            temp["pin"] = nuevo_pin
            with open("config.json", "w") as f:
                json.dump(obj=temp, fp=f)
            return True
        else:
            return False
    except:
        print("failed cuz tried to convert to int")
        return False

def reloj():
    return datetime.datetime.today()
