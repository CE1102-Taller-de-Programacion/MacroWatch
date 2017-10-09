import json
import datetime
import random


def confirma_pin(data):
    with open("config.json", "r") as f:
        config = json.load(fp=f)

    if data == config["pin"]:
        return True
    else:
        return False


class Persona:
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
        if i >= len(self.temp):
            return result
        else:
            result += [Persona(self.temp[i]["id"], self.temp[i]["nombre"],
                               self.temp[i]["telefonos"],
                               self.temp[i]["celular"],
                               self.temp[i]["correo"],
                               self.temp[i]["foto"])]

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
        se_elimino = self.eliminar_aux(identidad, 0)
        if se_elimino:
            self.contacts = self.sort_empty(0, [])
        return se_elimino

    def eliminar_aux(self, identidad, i):
        if i == len(self.contacts):
            return False
        elif self.contacts[i].identidad == identidad:
            self.contacts[i] = None
            return True
        else:
            return self.eliminar_aux(identidad, i+1)

    def sort_empty(self, i, result):
        """
        Sort que se encarga de remover los espacios vacíos una vez se elimina un
        contacto.
        """
        if i >= len(self.contacts):
            return result
        elif self.contacts[i] is not None:
            result += self.contacts[i]
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
            self.contacts = self.ordernar_id()
        elif modo == "Alfabético" or modo == "Alphabetical":
            self.contacts = self.ordenar_abc()

    def ordenar_id(self):
        return self.ordenar_id_aux(0, self.contacts, [])

    def ordenar_id_aux(self, i, copia, result):
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
        try:
            with open("contactos.json", "w") as f:
                json.dump(obj=self.temp, fp=f)
            return True
        except FileNotFoundError:
            return False


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

    def incluir(self, fecha, hora, info):
        self.agenda += Actividad(len(self.agenda), fecha, hora, info)

    def eliminar(self):
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

        with open("pal.json", "r") as f:
            load = json.load(fp=f)
        if not self.idi:
            i = random.randint(0, len(load["palabras"])-1)
            self.actual = load["palabras"][i]
        else:
            i = random.randint(0, len(load["words"])-1)
            self.actual = load["words"][i]

    def get_actual(self):
        return self.actual

    def get_adivinadas(self):
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

        elif letra in self.adivinadas:
            result = -1

        elif isinstance(letra, str) and letra in self.actual:
            self.adivinadas += letra
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

    # TODO: Hacer en shell para que no pueda enviar "palabra" vacío!!!
    def comprobar_palabra(self, palabra):
        """
        :param palabra: string
        :return: bool que indica si el usuario a logrado adivinar todas las letras
        de la palabra actual(self.actual).
        """
        return self.comprobar_palabra_aux(palabra, self.actual)

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
    return datetime.datetime.today()
