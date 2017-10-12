import WatchOs
import tkinter as tk

# Dict que contiene tuplas con texto a utilizar en español e inglés.
idi = {
    "pin": ("Ingrese su número PIN", "Enter your PIN number"),
    "exito": ("PIN válido", "Valid PIN"),
    "fallo": ("PIN invalido, pruebe de nuevo", "Invalid PIN, try again"),
    "opcion": ("Opciones", "Options"),
    "idioma": ("English", "Español"),
    "juego": ("Jugar", "Play Game"),
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
        subMenu.add_command(label=idi["idioma"][k], command=self.cambiar_idioma)
        subMenu.add_command(label=idi["juego"][k],
                            command=lambda: self.mostrar_app("AhorcadoUI"))
        subMenu.add_command(label=idi["pcambio"][k], command=self.Cambio)
        subMenu.add_command(label=idi["apagar"][k], command=self.apagar)

        self.apps = {}

        self.pila = tk.Frame(self.root)
        self.pila.grid(row=0, column=0, sticky="nsew")

        for i in (Main, AhorcadoUI, ContactosUI, AgendaUI):
            nombre = i.__name__
            app = i(master=self.root, controlador=self)
            self.apps[nombre] = app
            app.grid(row=0, column=0, sticky="nsew")

        self.mostrar_app("Main")

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
        self.test = tk.Label(master=self, text="Funciona")
        self.test.pack()
        self.contacts = tk.Button(self, text="Contactos", command=lambda: self.controlador.mostrar_app("ContactosUI"))
        self.contacts.pack()


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
        self.oid.grid(row=0, column=0, padx=60)
        self.oabc = tk.Button(self.left, text=f"{idi['oid'][k]}")
        self.oabc.grid(row=1, column=0, pady=30, padx=60)

        self.botones = [tk.Button(self.right, text="Recargar",
                                  command=lambda: self.display(0))]

        self.labels = self.display(0, [tk.Label(self.right, text=f"ID   {idi['contnombre'][k]}   {idi['conttel'][k]}   "
                                                                 f"{idi['contcel'][k]}   {idi['contcorreo'][k]}   "
                                                                 f"{idi['contfoto'][k]}"f"\n----------------"
                                                                 f"---------------------------------"
                                                                 f"--------------------", font=("Roboto", 10))])
        self.mostrar(0, 0, self.labels)

    def display(self, i, result):
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
        if i < len(labels):
            labels[i].grid(row=j, column=0, pady=0, sticky="W")
            self.botones[i].grid(row=j + 1, column=0, pady=10, sticky="W")
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


if __name__ == "__main__":
    Comienzo()
