import WatchOs
from tkinter import *
import time

# Dict que contiene tuplas con texto a utilizar en español e inglés.
idi = {
    "pin": ("Ingrese su número PIN", "Enter your PIN number"),
    "exito": ("PIN válido", "Valid PIN"),
    "fallo": ("PIN invalido, pruebe de nuevo", "Invalid PIN, try again"),
    "opcion": ("Opciones", "Options"),
    "idioma": ("Cambiar idioma", "Change language"),
    "juego": ("Jugar", "Play Game"),
    "pcambio": ("Cambiar PIN", "Change PIN"),
    "npin": ("Introduzca el nuevo PIN", "Enter the new PIN"),
    "cepin": ("¡Éxito!, el nuevo pin fue configurado", "Success!, the new pin has been configured"),
    "cfpin": ("Fallo, el pin no es válido o se perdió integridad de archivos",
              "Failure, the pin is not valid or file integrity is lost")
}

colores = {
    "activo": [],
    "inactivo": []
}

# Variable que determina el idioma actual, 0 = español / 1 = inglés
k = 0

# Variable que determina los colores de la interfaz según el estado de actividad, 0 = activo / 1 = inactivo
c = 0


class Comienzo:
    """
        Maneja el ingreso al sistema, aceptando una entrada que debe coincidir con el número de PIN.
    """
    def __init__(self):
        self.root = Tk()
        self.root.title(string="MacroWatch")
        self.root.iconbitmap(bitmap="watch.ico")
        self.root.geometry(newGeometry="250x75+500+200")
        self.intento = StringVar()
        self.login()
        self.root.mainloop()

    def login(self):
        """
            Muestra la interfaz para ingresar el PIN
        """
        login_info = Label(self.root, text=idi["pin"][k])
        login_info.pack()
        contrasena = Entry(self.root, textvariable=self.intento)
        contrasena.pack()
        contrasena.bind("<Return>", self.confirma)

    def confirma(self, *args):
        """
            :param args:

            Toma la entrada y la compara con el fin definido por el usuario
            (en caso de que el usuario no la haya cambiado, será el de fábrica)
            Y determina si coincide, si es el caso, ingresa al menú principal.
        """
        respuesta = StringVar()
        resutado = Label(self.root, textvariable=respuesta)
        resutado.pack()
        if WatchOs.confirma_pin(self.intento.get()):
            respuesta.set(idi["exito"][k])
            self.root.destroy()
            time.sleep(.5)
            Main()
        else:
            respuesta.set(idi["fallo"][k])


class Main:
    def __init__(self):
        self.root = Tk()
        self.root.geometry(newGeometry="450x500+500+100")
        self.root.title(string="MacroWatch")
        self.root.iconbitmap(bitmap="watch.ico")
        menu = Menu(master=self.root)
        self.root.config(menu=menu)
        subMenu = Menu(master=menu)
        menu.add_cascade(label=idi["opcion"][k], menu=subMenu)
        subMenu.add_command(label=idi["idioma"][k], command=self.cambiar_idioma)
        subMenu.add_command(label=idi["juego"][k], command=self.juego)
        subMenu.add_command(label=idi["pcambio"][k], command=self.Cambio)
        self.root.mainloop()

    def cambiar_idioma(self):
        global k
        if k:
            k = 0
        else:
            k = 1
        self.root.destroy()
        Main()

    class Cambio:
        def __init__(self):
            self.root = Tk()
            self.root.geometry("250x75+500+200")
            self.root.iconbitmap(bitmap="watch.ico")
            self.pin = StringVar(self.root)
            self.instruc = Label(master=self.root, text=idi["npin"][k])
            self.instruc.pack()
            self.nuevo = Entry(master=self.root, textvariable=self.pin)
            self.nuevo.pack()
            self.nuevo.bind("<Return>", func=self.cambiar_pin)

        def cambiar_pin(self, *args):
            if WatchOs.cambiar_pin(self.pin.get()):
                resultado = Label(self.root, text=idi["cepin"][k])
                resultado.pack()
            else:
                resultado = Label(self.root, text=idi["cefpin"][k])
                resultado.pack()

    def juego(self):
        AhorcadoUI()


class AhorcadoUI:
    def __init__(self):
        self.juego = WatchOs.Ahorcado(idi=k)
        self.palabra = self.juego.get_actual()
        self.root = Tk()
        self.root.title(string="MacroWatch")
        self.root.iconbitmap(bitmap="watch.ico")


class ContactosUI:
    def __init__(self, root):
        self.root = root
        self.root.title(string="MacroWatch")
        self.root.iconbitmap(bitmap="watch.ico")
        self.root.mainloop()


class AgendaUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("MacroWatch")
        self.root.iconbitmap(bitmap="watch.ico")
        self.root.mainloop()


if __name__ == "__main__":
    Comienzo()
