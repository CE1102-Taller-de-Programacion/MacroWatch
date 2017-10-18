import json
import datetime
import random
import calendar

# Partidas ganadas de ahorcado
ganadas = 0


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

    def crear(self, nombre, telefonos, celular, correo, foto):
        """
        :param nombre: str
        :param telefonos: array de ints
        :param celular: int
        :param correo: str
        :param foto: str
        :return: bool que indica el éxito de agregar el contacto.

        Agrega un usuario a la lista de contactos
        """
        self.contacts += [Persona(len(self.contacts), nombre, telefonos, celular, correo, foto)]
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
            self.contacts[i].identidad = len(result)
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
            return self.ordenar_id()
        elif modo == "Alfabético" or modo == "Alphabetical":
            return self.ordenar_abc()

    def ordenar_id(self):
        """
        :return: lista ya ordenada de contactos
        """
        return self.ordenar_id_aux(self.contacts, [])

    def ordenar_id_aux(self, copia, result):
        """
        :param i: int (índice)
        :param copia: lista de contactos
        :param result: lista de contactos ordenados
        """
        if not copia:
            return result
        else:
            temp = self.get_menor_id(0, 1, copia)
            i = copia.index(temp)
            result += [temp]
            if i != 1:
                return self.ordenar_id_aux(copia[0:i]+copia[i+1:len(copia)], result)
            else:
                return self.ordenar_id_aux(copia[1:], result)

    def get_menor_id(self, i, j, contactos):
        """
        :param i: indice de menor
        :param j: indice de posible mayor
        :param contactos: lista de personas
        :return: contacto con menor identidad en contactos
        """
        if j >= len(contactos):
            return contactos[i]
        elif contactos[i].identidad < contactos[j].identidad:
            return self.get_menor_id(i, j+1, contactos)
        elif contactos[i].identidad > contactos[j].identidad:
            return self.get_menor_id(j, j+1, contactos)

    def ordenar_abc(self):
        """
        :return: Lista con contactos ordenados alfabéticamente
        """
        return self.ordenar_abc_aux(self.contacts, [])

    def ordenar_abc_aux(self, copia, result):
        """
        :param copia: copia de lista contactos
        :param result:
        :return: lista con contactos ordenado alfabéticamente
        """
        if not copia:
            return result
        else:
            temp = self.get_menor_abc(0, 1, 0, copia)
            i = copia.index(temp)
            result += [temp]
            if i != 0:
                return self.ordenar_abc_aux(copia[0:i] + copia[i + 1:len(copia)], result)
            else:
                return self.ordenar_abc_aux(copia[1:], result)

    def get_menor_abc(self, i, j, k, contactos):
        """
        :param i: indice de mejor
        :param j: indice de posible mayor
        :param k: indice para letra de comparación
        :param contactos: lista de contactos
        :return: contacto con el nombre menor en el alfabeto
        """
        if j >= len(contactos):
            return contactos[i]
        elif contactos[i].nombre[k] < contactos[j].nombre[k]:
            return self.get_menor_abc(i, j+1, 0, contactos)
        elif contactos[i].nombre[k] > contactos[j].nombre[k]:
            return self.get_menor_abc(j, j+1, 0, contactos)
        elif contactos[i].nombre[k] == contactos[j].nombre[k]:
            return self.get_menor_abc(i, j, k+1, contactos)

    def seleccionar(self, identidad):
        """
        :param identidad: identidad del contacto a seleccionar
        :return: contacto con la identidad correspondiente
        """
        return self.seleccionar_aux(int(identidad), 0)

    def seleccionar_aux(self, identidad, i):
        """
        :param identidad: identidad del contacto a seleccionar
        :param i: indice para atraversar self.contacts
        :return: contacto con la identidad correspindiente
        """
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
                json.dump(obj=self.lista_dictionary(0, {}), fp=f)
            return True
        except FileNotFoundError:
            return False

    def lista_dictionary(self, i, result):
        """
        :param i: int índice
        :param result: dictionario que será guardado en disco
        :return: result
        """
        if i >= len(self.contacts):
            return result
        else:
            result[i] = {"id": str(self.contacts[i].identidad),
                                                       "nombre": self.contacts[i].nombre,
                                                       "telefonos": self.contacts[i].telefonos,
                                                       "celular": self.contacts[i].celular,
                                                       "correo": self.contacts[i].correo,
                                                       "foto": self.contacts[i].foto}

            return self.lista_dictionary(i+1, result)


class Actividad:
    def __init__(self, identidad, fecha, hora, info):
        """
        :param identidad: identidad de la actividad particular
        :param fecha: fecha del evento
        :param hora: hora del evento
        :param info: descripción del evento
        Objeto que guarda un evento particular.
        """
        self.identidad = identidad
        self.fecha = fecha
        self.hora = hora
        self.info = info


class Agenda:
    def __init__(self):
        """
        Carga actividades en disco
        """
        with open("agenda.json", "r") as f:
            self.agenda = json.load(fp=f)
            self.agenda = self.cargar(0, [])

    def cargar(self, i, result):
        """
        :param i:
        :param result:
        :return: lista de actividades
        Transforma el objeto json en una lista de objetos Actividad
        """
        if i == len(self.agenda):
            return result
        else:
            j = str(i)
            result += [Actividad(i, self.agenda[j]["fecha"], self.agenda[j]["hora"], self.agenda[j]["info"])]

            return self.cargar(i+1, result)

    def incluir(self, fecha, hora, info):
        """
        :param fecha:
        :param hora:
        :param info:
        Incluye un nuevo evento a la lista
        """
        self.agenda += [Actividad(len(self.agenda), fecha, hora, info)]

    def eliminar(self, identidad):
        """
        :param identidad:

        Elimina la actividad correspondiente y vuelve a ordenar la lista para evitar tener espacios null
        vacíos.
        """
        try:
            self.agenda[identidad] = None
            self.agenda = self.sort_empty(0, [])
            return True

        except KeyError:
            return False

    def sort_empty(self, i, result):
        """
        Sort que se encarga de remover los espacios vacíos una vez se elimina un
        contacto.
        """
        if i >= len(self.agenda):
            return result
        elif self.agenda[i] is not None:
            self.agenda[i].identidad = len(result)
            result += [self.agenda[i]]
            return self.sort_empty(i + 1, result)
        else:
            return self.sort_empty(i + 1, result)

    def cambiar_fecha(self, identidad, nueva_fecha):
        """
        :param identidad:
        :param nueva_fecha:
        :return: bool que indica si fue exitosa la operación
        Cambia la fecha de un evento particular
        """
        try:
            i = self.agenda.index(identidad)
            self.agenda[i].fecha = nueva_fecha
            return True

        except IndexError:
            return False

    def cambiar_hora(self, identidad, nueva_hora):
        """
        :param identidad:
        :param nueva_hora:
        :return: bool que indica si fue exitosa la operación
        Cambia la hora de un evento particular
        """
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

    def save(self):
        """
        :return: bool que indica si la operación fue exitosa

        Guarda self.contacts a disco
        """
        try:
            with open("agenda.json", "w") as f:
                json.dump(obj=self.lista_dictionary(0, {}), fp=f)
            return True
        except FileNotFoundError:
            return False

    def lista_dictionary(self, i, result):
        """
        :param i: int índice
        :param result: dictionario que será guardado en disco
        :return: result
        """
        if i >= len(self.agenda):
            return result
        else:
            result[i] = {"id": str(self.agenda[i].identidad),
                         "fecha": self.agenda[i].fecha,
                         "hora": self.agenda[i].hora,
                         "info": self.agenda[i].info
                         }

            return self.lista_dictionary(i + 1, result)


class Ahorcado:
    """
    Clase que maneja la lógica para el juego de ahorcado
    Genera la palabra a utilizar y comprueba cada vez que se le pide
    """

    def __init__(self, idi):
        global ganadas
        self.idi = idi
        self.adivinadas = ""
        self.equivocadas = ""
        self.intentos = 8

        with open("pal.json", "r") as f:
            load = json.load(fp=f)
        if not self.idi:
            i = random.randint(0, len(load["palabras"])-1)
            self.actual = load["palabras"][i]
        else:
            i = random.randint(0, len(load["words"])-1)
            self.actual = load["words"][i]

        ganadas = load["ganadas"]

    def get_actual(self):
        """
        :return: str, palabra uilizada en juego actual.
        """
        return self.actual

    def get_adivinadas(self):
        """
        :return: lista de str, letras ya adivinadas.
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
        """
        :param i:
        :param letra:
        :param pos:
        :param result:
        :return: la cantidad de veces la letra en particular aparece en self.actual
        """
        if i >= len(pos):
            return result
        else:
            result += [letra]
            return self.cantidad_letras(i+1, letra, pos, result)

    def comprobar_palabra(self):
        """
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

    def salvar(self):
        """
        Guarda el gane en disco
        """
        with open("pal.json", "r") as f:
            temp = json.load(fp=f)
        temp["ganadas"] = ganadas
        with open("pal.json", "w") as f:
            json.dump(obj=temp, fp=f)


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
    except:
        return False


def get_idioma():
    """
    :return: Devuelve el idioma de preferencia del usuario
    """
    with open("config.json", "r") as f:
        temp = json.load(fp=f)
    return temp["idioma"]


def set_idioma(idioma):
    """
    :param idioma:
    :return: Guarda el idioma de preferencia en disco
    """
    with open("config.json", "r") as f:
        temp = json.load(fp=f)
    temp["idioma"] = idioma
    with open("config.json", "w") as f:
        json.dump(obj=temp, fp=f)


def get_date():
    """
    :return: La fecha actual en formato texto
    """
    ahora = get_time()
    return f"{calendar.month_name[ahora.month]} {ahora.day}, {ahora.year}"


def get_time():
    """
    :return: El tiempo y fecha actuales
    """
    return datetime.datetime.now()
