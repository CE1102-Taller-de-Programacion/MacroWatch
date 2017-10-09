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
    "apagar": ("Apagar", "Turn off")
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
            Muestra la interfaz para ingresar el PIN
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
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(newGeometry="550x500+500+100")
        self.root.title(string="MacroWatch")
        self.root.iconbitmap(bitmap="watch.ico")
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

    class Cambio:
        def __init__(self):
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
        global k
        if k:
            k = 0
        else:
            k = 1
        self.root.destroy()
        Controlador()

    def mostrar_app(self, nombre):
        app = self.apps[nombre]
        app.tkraise()


class Main(tk.Frame):
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.controlador = controlador
        self.test = tk.Label(master=self, text="Funciona")
        self.test.pack()


class AhorcadoUI(tk.Frame):
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.controlador = controlador
        self.juego = WatchOs.Ahorcado(idi=k)
        self.palabra = self.juego.get_actual()
        self.test = tk.Label(self, text="Funciona")
        self.test.pack()


class ContactosUI(tk.Frame):
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.controlador = controlador


class AgendaUI(tk.Frame):
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.controlador = controlador


if __name__ == "__main__":
    Comienzo()
