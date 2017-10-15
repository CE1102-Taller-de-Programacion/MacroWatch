import json
import datetime
import random
import time


def confirma_pin(data):
    """
    :param data:
    :return: bool que indica si el PIN es correcto.

    Abre el archivo de configuración para recolectar el pin, el cual es comparado el ingresado por el usuario.
    """
    with open("config.json", "r") as f:
        config = json.load(fp=f)

    if data == config["pin"]:
        return True
    else:
        return False


class Persona:
    """
    Struct que contiene los atributos de un individuo.
    """
    def __init__(self, identidad, nombre, telefonos, celular, correo, foto):
        self.identidad = identidad
        self.nombre = nombre
        self.telefonos = telefonos
        self.celular = celular
        self.correo = correo
        self.foto = foto


class Contactos:
    """
        Maneja, muestra y administra los contactos del sistema.
    """
    def __init__(self):
        # Carga los contactos del disco.
        with open("contactos.json", "r") as f:
            self.temp = json.load(fp=f)

        self.contacts = self.cargar(0, [])

    def cargar(self, i, result):
        """
        :param i: índice que carga contactos hasta el final del dict.
        :param result: lista que sostiene todos los contactos una vez cargados
        :return: result si ya termino / self si aún faltan contactos
        """
        if i >= len(self.temp):
            return result
        else:
            j = str(i)
            result += [Persona(self.temp[j]["id"], self.temp[j]["nombre"],
                               self.temp[j]["telefonos"],
                               self.temp[j]["celular"],
                               self.temp[j]["correo"],
                               self.temp[j]["foto"])]

            return self.cargar(i+1, result)

    def crear(self, identidad, nombre, telefonos, celular, correo, foto):
        """
        :param identidad: int
        :param nombre: str
        :param telefonos: array de ints
        :param celular: int
        :param correo: str
        :param foto: str
        :return: bool que indica el éxito de agregar el contacto.

        Agrega un usuario a la lista de contactos
        """
        self.contacts += [Persona(identidad, nombre, telefonos, celular, correo, foto)]
        return True

    def eliminar(self, identidad):
        """
        :param identidad:

        Elimina el usuario con la identidad correspondiente y vuelve a ordenar la lista para evitar tener espacios
        vacíos.
        """
        try:
            self.contacts[identidad] = None
            self.contacts = self.sort_empty(0, [])
            return True

        except KeyError:
            return False

    def sort_empty(self, i, result):
        """
        Sort que se encarga de remover los espacios vacíos una vez se elimina un
        contacto.
        """
        if i >= len(self.contacts):
            return result
        elif self.contacts[i] is not None:
            result += [self.contacts[i]]
            return self.sort_empty(i + 1, result)
        else:
            return self.sort_empty(i + 1, result)

    def ordenar(self, modo):
        """
        :param modo
        :return: result

        Genera un lista copia de contactos, el cual se ordena con Selection Sort según el modo especificado.
        """
        if modo == "ID":
            self.contacts = self.ordenar_id()
        elif modo == "Alfabético" or modo == "Alphabetical":
            self.contacts = self.ordenar_abc()

    def ordenar_id(self):
        """
        :return: lista ya ordenada de contactos
        """
        return self.ordenar_id_aux(0, self.contacts, [])

    def ordenar_id_aux(self, i, copia, result):
        """
        :param i: int (índice)
        :param copia: lista de contactos
        :param result: lista de contactos ordenados
        """
        if i == len(copia):
            return result
        else:
            j = self.get_index_min(copia, 0, int(copia[0].identidad))
            result += [self.contacts[j]]
            return self.ordenar_id_aux(i+1, copia[0:j]+copia[j+1:len(copia)], result)

    def get_index_min(self, temp, i, result):
        if i == len(temp):
            return result
        elif int(temp[i].identidad) < result:
            return self.get_index_min(temp, i+1, temp[i])
        else:
            return self.get_index_min(temp, i+1, result)

    def seleccionar(self, identidad):
        return self.seleccionar_aux(int(identidad), 0)

    def seleccionar_aux(self, identidad, i):
        if i == len(self.contacts):
            return False
        elif self.contacts[i].identidad == identidad:
            return self.contacts[i]
        else:
            return False

    def save(self):
        """
        :return: bool que indica si la operación fue exitosa

        Guarda self.contacts a disco
        """
        try:
            with open("contactos.json", "w") as f:
                json.dump(obj=self.lista_dictionary(len(self.contacts)-1, {}), fp=f)
            return True
        except FileNotFoundError:
            return False

    def lista_dictionary(self, i, result):
        """
        :param i: int índice
        :param result: dictionario que será guardado en disco
        :return: result
        """
        if i == 0:
            return result
        else:
            result[str(self.contacts[i].identidad)] = {"id": str(self.contacts[i].identidad),
                                                       "nombre": self.contacts[i].nombre,
                                                       "telefonos": self.contacts[i].telefonos,
                                                       "celular": self.contacts[i].celular,
                                                       "correo": self.contacts[i].correo,
                                                       "foto": self.contacts[i].foto}

            return self.lista_dictionary(i-1, result)


# Kinda done
class Calculadora:
    def suma(self, num_array):
        return self.suma_aux(num_array, 0)

    def suma_aux(self, num_array, result):
        if not num_array:
            return result
        else:
            result += int(num_array[0])
            return self.suma_aux(num_array[1:], result)

    def resta(self, num_array):
        return self.resta_aux(num_array, 0)

    def resta_aux(self, num_array, result):
        if not num_array:
            return result
        else:
            result -= int(num_array[0])
            return self.resta_aux(num_array[1:], result)

    def producto(self, num_array):
        return self.producto_aux(num_array, 0)

    def producto_aux(self, num_array, result):
        if not num_array:
            return result
        else:
            result *= int(num_array[0])
            return self.producto_aux(num_array[1:], result)

    def division(self, num_array):
        return self.division_aux(num_array, 0)

    def division_aux(self, num_array, result):
        if not num_array:
            return result
        else:
            result += int(num_array[0])
            return self.division_aux(num_array[1:], result)


# DONE
class Actividad:
    def __init__(self, identidad, fecha, hora, info):
        self.identidad = identidad
        self.fecha = fecha
        self.hora = hora
        self.info = info


class Agenda:
    def __init__(self):
        with open("agenda.json", "r") as f:
            self.agenda = json.load(fp=f)
            self.agenda = self.cargar(0, [])

    def cargar(self, i, result):
        if i == len(self.agenda):
            return result
        else:
            j = str(i)
            result += [Actividad(i, self.agenda[j]["fecha"], self.agenda[j]["hora"], self.agenda[j]["info"])]

            return self.cargar(i+1, result)

    def incluir(self, fecha, hora, info):
        self.agenda += [Actividad(len(self.agenda), fecha, hora, info)]

    def eliminar(self):
        # TODO
        pass

    def cambiar_fecha(self, identidad, nueva_fecha):
        try:
            i = self.agenda.index(identidad)
            self.agenda[i].fecha = nueva_fecha
            return True

        except IndexError:
            return False

    def cambiar_hora(self, identidad, nueva_hora):
        try:
            i = self.agenda.index(identidad)
            self.agenda[i].hora = nueva_hora
            return True

        except IndexError:
            return False

    def mostrar(self):
        """
        :return: Lista de Actividades
        """
        return self.agenda


# DONE
class Ahorcado:
    """
    Clase que maneja la lógica para el juego de ahorcado
    Genera la palabra a utilizar y comprueba cada vez que se le pide
    """
    def __init__(self, idi):
        self.idi = idi
        self.adivinadas = ""
        self.equivocadas = ""

        with open("pal.json", "r") as f:
            load = json.load(fp=f)
        if not self.idi:
            i = random.randint(0, len(load["palabras"])-1)
            self.actual = load["palabras"][i]
        else:
            i = random.randint(0, len(load["words"])-1)
            self.actual = load["words"][i]

    def get_actual(self):
        """
        :return: str, palabra uilizada en juego actual.
        """
        return self.actual

    def get_adivinadas(self):
        """
        :return: lista de str, letras ya adivinadas
        """
        return self.adivinadas

    def comprobar_letra(self, letra):
        """
        Condiciones: Entrada debe ser str de longitud 1 que se encuentra en self.actual.
        :param letra: char
        :return: int que indica si la letra dada por el usuario está en la
        palabra actual y cumple las condiciones.
        """
        result = 0
        if len(letra) != 1:
            pass

        elif letra not in self.actual and letra not in self.equivocadas:
            self.equivocadas += letra
            result = -1

        elif letra in self.adivinadas or letra in self.equivocadas:
            result = -2

        elif letra in self.actual:
            lista_letra = self.cantidad_letras(0, letra, self.pos(letra, 0, []), [])
            hil_letra = "".join(lista_letra)
            self.adivinadas += hil_letra
            result = 1

        return result

    def pos(self, letra, i, result):
        """
        :param letra: Letra ingresada por el usuario
        :param i: índice para recorrer caracteres en self.actual
        :param result: lista donde se pondrán posiciones
        :return: posiciones donde se encuentra la letra en self.actual
        """
        if i >= len(self.actual):
            return result
        elif self.actual[i] == letra:
            return self.pos(letra, i + 1, result + [i])
        else:
            return self.pos(letra, i + 1, result)

    def cantidad_letras(self, i, letra, pos, result):
        if i >= len(pos):
            return result
        else:
            result += [letra]
            return self.cantidad_letras(i+1, letra, pos, result)

    # TODO: Hacer en shell para que no pueda enviar "palabra" vacío!!!
    def comprobar_palabra(self):
        """
        :param palabra: string
        :return: bool que indica si el usuario a logrado adivinar todas las letras
        de la palabra actual(self.actual).
        """
        return self.comprobar_palabra_aux(self.adivinadas, self.actual)

    def comprobar_palabra_aux(self, palabra, temp):
        if (not palabra and temp) or (palabra and not temp):
            return False

        elif not palabra and not temp:
            return True

        elif palabra[0] in temp:
            i = temp.index(palabra[0])
            return self.comprobar_palabra_aux(palabra[1:], temp[0:i]+temp[i+1:len(temp)])

        else:
            return False


def cambiar_pin(nuevo_pin):
    """
    :param nuevo_pin: int
    :return: bool que indica si la operación fue exitosa
    """
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
    # TODO: Especificar except.
    except:
        return False


def get_time():
    return datetime.datetime.now()
