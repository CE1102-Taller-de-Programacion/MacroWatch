import WatchOs
import tkinter as tk
from PIL import ImageTk
from PIL import Image

# Dict que contiene tuplas con texto a utilizar en español e inglés.
idi = {
    "pin": ("Ingrese su número PIN", "Enter your PIN number"),
    "exito": ("PIN válido", "Valid PIN"),
    "fallo": ("PIN invalido, pruebe de nuevo", "Invalid PIN, try again"),
    "opcion": ("Opciones", "Options"),
    "idioma": ("English", "Español"),
    "menup": ("Menu Principal", "Main Menu"),
    "pcambio": ("Cambiar PIN", "Change PIN"),
    "npin": ("Introduzca el nuevo PIN", "Enter the new PIN"),
    "cepin": ("¡Éxito!, el nuevo PIN fue configurado", "Success!, the new PIN has been configured"),
    "cfpin": ("Fallo, el PIN no es válido o se perdió integridad de archivos",
              "Failure, the PIN is not valid or file integrity is lost"),
    "apagar": ("Apagar", "Turn off"),
    "letra": ("Ingrese una letra", "Enter a letter"),
    "restantes": ("Intentos Restantes:", "Attempts left:"),
    "contnombre": ("Nombre", "Name"),
    "conttel": ("Teléfonos", "Telephone"),
    "contcel": ("Celular", "Cellphone"),
    "contcorreo": ("Correo", "eMail"),
    "contfoto": ("Foto", "Photo"),
    "agenfecha": ("Fecha", "Date"),
    "agenhora": ("Hora", "Time"),
    "agenevento": ("Evento", "Event"),
    "delcont": ("Eliminar Contacto", "Delete contact"),
    "oid": ("Ordenar por ID", "Sort by ID"),
    "oabc": ("Ordenar por nombre", "Sort by name")
}

colores = {
    "activo": [],
    "inactivo": []
}

# Variable que determina el idioma actual, 0 = español / 1 = inglés
k = 0

# Variable que determina los colores de la interfaz según el estado de actividad, 0 = activo / 1 = inactivo
c = 0


# TODO intro animación
class Comienzo:
    """
        Maneja el ingreso al sistema, aceptando una entrada que debe coincidir con el número de PIN.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(string="MacroWatch")
        self.root.iconbitmap(bitmap="watch.ico")
        self.root.geometry(newGeometry="250x75+500+200")
        self.intento = tk.StringVar()
        self.login()
        self.root.mainloop()

    def login(self):
        """
           Crea la entrada donde el usuario puede ingresar su PIN
        """
        login_info = tk.Label(self.root, text=idi["pin"][k])
        login_info.pack()
        contrasena = tk.Entry(self.root, textvariable=self.intento)
        contrasena.pack()
        contrasena.bind("<Return>", self.confirma)

    def confirma(self, *args):
        """
        :param args:

        Toma la entrada y la compara con el fin definido por el usuario
        (en caso de que el usuario no la haya cambiado, será el de fábrica)
        Y determina si coincide, si es el caso, ingresa al menú principal.
        """
        respuesta = tk.StringVar()
        resutado = tk.Label(self.root, textvariable=respuesta)
        resutado.pack()
        if WatchOs.confirma_pin(self.intento.get()):
            respuesta.set(idi["exito"][k])
            self.root.destroy()
            Controlador()
        else:
            respuesta.set(idi["fallo"][k])


class Controlador:
    """
    Crea y administra las frames de la aplicación, así como brindar el menu superior
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(newGeometry="600x500+500+100")
        self.root.title(string="MacroWatch")
        self.root.iconbitmap(bitmap="watch.ico")
        self.root.resizable(False, False)
        menu = tk.Menu(master=self.root)
        self.root.config(menu=menu)
        subMenu = tk.Menu(master=menu)
        menu.add_cascade(label=idi["opcion"][k], menu=subMenu)
        subMenu.add_command(label=idi["menup"][k], command=lambda: self.mostrar_app("Main"))
        subMenu.add_separator()
        subMenu.add_command(label=idi["idioma"][k], command=self.cambiar_idioma)
        subMenu.add_command(label=idi["pcambio"][k], command=self.Cambio)
        subMenu.add_command(label=idi["apagar"][k], command=self.apagar)

        self.apps = {}

        self.pila = tk.Frame(self.root)
        self.pila.grid(row=0, column=0, sticky="nsew")

        self.clases = [Main, AhorcadoUI, ContactosUI, AgendaUI, CalculadoraUI]

        self.cargar_apps(0)

        self.mostrar_app("Main")

    def cargar_apps(self, i):
        if i < len(self.clases):
            nombre = self.clases[i].__name__
            app = self.clases[i](master=self.root, controlador=self)
            self.apps[nombre] = app
            app.grid(row=0, column=0, sticky="nswe")

            self.cargar_apps(i+1)

    class Cambio:
        def __init__(self):
            """
            Provee una interfaz para que el usuario cambie el pin del dispositivo
            """
            self.root = tk.Tk()
            self.root.title(string=idi["pcambio"][k])
            self.root.geometry("250x75+500+200")
            self.root.iconbitmap(bitmap="watch.ico")
            self.pin = tk.StringVar(self.root)
            self.instruc = tk.Label(master=self.root, text=idi["npin"][k])
            self.instruc.pack()
            self.nuevo = tk.Entry(master=self.root, textvariable=self.pin)
            self.nuevo.pack()
            self.nuevo.bind("<Return>", func=self.cambiar_pin)

        def cambiar_pin(self, *args):
            """
            :param args:
            :Restricciones Debe ser un int y estar entre el rango de ]0,9999]
            Cambia el pin de acceso en disco.
            """
            if WatchOs.cambiar_pin(self.pin.get()):
                resultado = tk.Label(self.root, text=idi["cepin"][k])
                resultado.pack()
            else:
                resultado = tk.Label(self.root, text=idi["cfpin"][k])
                resultado.pack()

    def apagar(self):
        # TODO outro animación
        # TODO Guardar datos antes de cerrar
        """
        Llama las funciones que se encargan de guardar los datos y apagar el sistema.
        """
        self.root.destroy()

    def cambiar_idioma(self):
        """
        Cambia el idioma de la interfaz -Provoca que la ventana se cierre y abra-
        """
        global k
        if k:
            k = 0
        else:
            k = 1
        self.root.destroy()
        Controlador()

    def mostrar_app(self, nombre):
        """
        :param nombre: str, nombre de la app que se quiere mostrar en la interfaz
        Alza la frame que sea desea mostrar por encima del resto.
        """
        app = self.apps[nombre]
        app.tkraise()


class Main(tk.Frame):
    """
    Interfaz principal del reloj
    """
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.controlador = controlador

        # Botón hacia contactos
        image1 = Image.open("imagenes/contactos.png")
        image1 = image1.resize((50, 50), Image.ANTIALIAS)
        self.conticon = ImageTk.PhotoImage(image1)

        self.contacts = tk.Button(self, command=lambda: self.controlador.mostrar_app("ContactosUI"))
        self.contacts.place(x=50, y=300)
        self.contacts.config(image=self.conticon)

        # Botón hacia agenda
        image2 = Image.open("imagenes/agenda.png")
        image2 = image2.resize((50, 50), Image.ANTIALIAS)
        self.agenicon = ImageTk.PhotoImage(image2)

        self.agenda = tk.Button(self, command=lambda: self.controlador.mostrar_app("AgendaUI"))
        self.agenda.place(x=150, y=300)
        self.agenda.config(image=self.agenicon)

        # Botón hace calculadora
        image3 = Image.open("imagenes/calculadora.png")
        image3 = image3.resize((50, 50), Image.ANTIALIAS)
        self.calcicon = ImageTk.PhotoImage(image3)

        self.calculadora = tk.Button(self, command=lambda: self.controlador.mostrar_app("CalculadoraUI"))
        self.calculadora.place(x=250, y=300)
        self.calculadora.config(image=self.calcicon)

        # Botón hacia ahorcado
        image4 = Image.open("imagenes/ahorcado.png")
        image4 = image4.resize((50, 50), Image.ANTIALIAS)
        self.ahorcicon = ImageTk.PhotoImage(image4)

        self.ahorcado = tk.Button(self, command=lambda: self.controlador.mostrar_app("AhorcadoUI"))
        self.ahorcado.place(x=350, y=300)
        self.ahorcado.config(image=self.ahorcicon)

        # Genera label que representa el reloj
        self.reloj = tk.Label(master=self, text=f"{WatchOs.get_time().hour}:{WatchOs.get_time().minute}")
        self.reloj.place(x=250, y=250)
        self.actualizar()

    def actualizar(self):
        """
        Actualiza el reloj por segundo.
        """
        self.reloj.config(text=f'{WatchOs.get_time().hour}:{WatchOs.get_time().minute}:'
                               f'{WatchOs.get_time().second}')

        self.reloj.after(1000, lambda: self.actualizar())


class AhorcadoUI(tk.Frame):
    """
    Interfaz para el juego de ahorcado
    """
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.controlador = controlador
        self.juego = WatchOs.Ahorcado(idi=k)
        self.palabra = self.juego.get_actual()
        self.intentos = tk.IntVar()
        self.intentos.set(value=len(self.palabra) - 1)

        self.pedido = tk.Label(self, text=idi["letra"][k])
        self.pedido.grid(row=0, column=0, pady=5, sticky="W")
        self.restantes = tk.Label(self, text=idi["restantes"][k])
        self.restantes.grid(row=0, column=1, padx=20)
        self.mostrar_intentos = tk.Label(self, textvariable=self.intentos)
        self.mostrar_intentos.grid(row=0, column=2, padx=5)
        self.guarda_letra = tk.StringVar()
        self.entrada = tk.Entry(self)
        self.entrada.bind("<Return>", func=lambda: self.juego.comprobar_letra(self.guarda_letra))
        self.entrada.grid(row=1, column=0, sticky="S")


class ContactosUI(tk.Frame):
    """
    Interfaz para mostrar contactos
    """

    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.right = tk.Frame(self)
        self.right.grid(row=0, column=1)
        self.left = tk.Frame(self)
        self.left.grid(row=0, column=0)
        self.controlador = controlador
        self.contactos = WatchOs.Contactos()
        self.oid = tk.Button(self.left, text=f"{idi['oabc'][k]}")
        self.oid.grid(row=0, column=0, sticky="n")
        self.oabc = tk.Button(self.left, text=f"{idi['oid'][k]}")
        self.oabc.grid(row=1, column=0, sticky="n")

        self.botones = [None]

        self.labels = self.display(0, [tk.Label(self.right, text=f"ID   {idi['contnombre'][k]}   {idi['conttel'][k]}   "
                                                                 f"{idi['contcel'][k]}   {idi['contcorreo'][k]}   "
                                                                 f"{idi['contfoto'][k]}"f"\n----------------"
                                                                 f"---------------------------------"
                                                                 f"--------------------", font=("Roboto", 10))])
        self.mostrar(0, 0, self.labels)

    def display(self, i, result):
        """
        :param i:
        :param result:
        :return: llena listas con las widgets necesarias para mostrar.
        """
        conts = self.contactos.contacts
        if i < len(self.contactos.contacts):
            result += [tk.Label(self.right, text=f"{conts[i].identidad}   {conts[i].nombre}   "
                                                 f"{conts[i].telefonos}   {conts[i].celular}   {conts[i].correo}   "
                                                 f"{conts[i].foto}", font=("Roboto", 10))]

            self.botones += [
                tk.Button(self.right, text=f"{idi['delcont'][k]}", command=lambda: self.contactos.eliminar(i),
                          font=("Roboto", 8))]
            return self.display(i + 1, result)
        else:
            return result

    def mostrar(self, i, j, labels):
        """
        :param i: int, índice de elmento
        :param j: int, índice de ordenamiento
        :param labels: lista de Labels
        Muestra los contactos en la interfaz
        """
        if 0 < i < len(labels):
            labels[i].grid(row=j, column=0, pady=0, sticky="W")
            self.botones[i].grid(row=j + 1, column=0, pady=10, sticky="W")
            self.mostrar(i + 1, j + 2, labels)
        elif i < len(labels):
            labels[i].grid(row=j, column=0, pady=0, sticky="W")
            self.mostrar(i + 1, j + 2, labels)


class AgendaUI(tk.Frame):
    """
    Interfaz para mostrar agenda
    """

    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.controlador = controlador
        self.actividades = WatchOs.Agenda()
        self.labels = self.display(0, [tk.Label(self,
                                                text=f"ID   {idi['agenfecha'][k]}   {idi['agenhora'][k]}   "
                                                     f"{idi['agenevento'][k]}"
                                                     f"\n----------------------------------"
                                                     f"-----------------------------------", font=("Roboto", 10))])
        self.mostrar(0, self.labels)

    def display(self, i, result):
        actv = self.actividades.agenda
        if i < len(actv):
            result += [tk.Label(self, text=f"{actv[i].identidad}   {actv[i].fecha}   {actv[i].hora}   "
                                           f"{actv[i].info}", font=("Roboto", 10))]
            return self.display(i + 1, result)
        else:
            return result

    def mostrar(self, i, labels):
        if i < len(labels):
            labels[i].grid(row=i, column=0, padx=5)

            self.mostrar(i + 1, labels)


class CalculadoraUI(tk.Frame):
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)


if __name__ == "__main__":
    Comienzo()
