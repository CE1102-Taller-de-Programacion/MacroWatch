import WatchOs
import tkinter as tk
from PIL import ImageTk
from PIL import Image
import threading
from itertools import count
import parser


# Dict que contiene tuplas con texto a utilizar en español e inglés.
idi = {
    "pin": ("Ingrese su número PIN", "Enter your PIN number"),
    "prender": ("Encender", "Turn on"),
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
    "letra": ("Ingrese su intento", "Enter your guess"),
    "restantes": ("Intentos Restantes:", "Attempts left:"),
    "contnombre": ("Nombre", "Name"),
    "conttel": ("Teléfono", "Telephone"),
    "contcel": ("Celular", "Cellphone"),
    "contcorreo": ("Correo", "eMail"),
    "contfoto": ("Foto", "Photo"),
    "agenfecha": ("Fecha", "Date"),
    "agenhora": ("Hora", "Time"),
    "agenevento": ("Evento", "Event"),
    "delcont": ("Eliminar Contacto", "Delete contact"),
    "oid": ("Ordenar por ID", "Sort by ID"),
    "oabc": ("Ordenar por nombre", "Sort by name"),
    "badivina": ("¡Bien adivinado!", "Good guess!"),
    "madivina": ("Mal adivinado", "Bad guess"),
    "noletra": ("Entrada no es una letra", "Entry is not a letter"),
    "readivina": ("Ya adivinó esa letra...", "Already guessed that letter..."),
    "aganador": ("¡FELICIDADES, HA GANADO!", "WINNER WINNER, CHICKEN DINNER!"),
    "aperdedor": ("Ha perdido", "You have lost"),
    "greiniciar": ("Reiniciar Juego", "Restart Game"),
    "idselect": ("Seleccionar contacto", "Select contact"),
    "cagregar": ("Agregar contacto", "Add contact"),
    "correo": ("Correo", "Email"),
    "foto": ("Foto", "Photo"),
    "agregar": ("Agregar", "Add"),
    "nombre": ("Nombre", "Name"),
    "amostrar": ("Seleccionar fecha", "Select date"),
    "adel": ("Eliminar evento", "Delete event"),
    "afecha": ("Cambiar fecha", "Change date"),
    "ahora": ("Cambiar hora", "Change time"),
    "aincluir": ("Incluir evento", "Include event"),
    "ganadas": ("Partidas Ganadas:", "Won Matches:"),
    "regresar": ("Regresar", "Go back"),
    "descansa": ("Descansador", "Screen Saver")
}

# Variable que determina el idioma actual, 0 = español / 1 = inglés
z = WatchOs.get_idioma()


class Comienzo:
    """
        Maneja el ingreso al sistema, aceptando una entrada que debe coincidir con el número de PIN.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(string="MacroWatch")
        self.root.iconbitmap(bitmap="imagenes/watch.ico")
        self.root.geometry(newGeometry="250x120+550+300")
        self.root.config(bg="#212121")
        self.intento = tk.StringVar()
        self.respuesta = tk.StringVar()
        self.resultado = tk.Label(self.root, textvariable=self.respuesta, bg="#212121", fg="#ffffff")
        self.resultado.place(x=45, y=85)
        self.login()
        self.root.mainloop()

    def login(self):
        """
           Crea la entrada donde el usuario puede ingresar su PIN
        """
        login_info = tk.Label(self.root, text=idi["pin"][z], bg="#212121", fg="#ffffff")
        login_info.place(x=65, y=0)
        contrasena = tk.Entry(self.root, textvariable=self.intento)
        contrasena.place(x=65, y=30)
        contrasena.bind("<Return>", self.confirma)
        prender = tk.Button(self.root, text=idi["prender"][z], command=self.confirma, borderwidth=0,
                            bg="#212121", fg="#33b5e5")
        prender.place(x=97, y=60)

    def confirma(self, *args):
        """
        :param args:

        Toma la entrada y la compara con el fin definido por el usuario
        (en caso de que el usuario no la haya cambiado, será el de fábrica)
        Y determina si coincide, si es el caso, ingresa al menú principal.
        """
        if WatchOs.confirma_pin(self.intento.get()):
            self.respuesta.set(idi["exito"][z])
            self.root.destroy()
            Controlador()
        else:
            self.respuesta.set(idi["fallo"][z])


class Controlador:
    """
    Crea y administra las frames de la aplicación, así como brindar el menu superior
    """

    # noinspection PyPep8Naming
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(newGeometry="600x500+400+100")
        self.root.title(string="MacroWatch")
        self.root.iconbitmap(bitmap="imagenes/watch.ico")
        self.root.resizable(width=False, height=False)

        menu = tk.Menu(master=self.root)
        self.root.config(menu=menu)
        subMenu = tk.Menu(master=menu, bg="#212121", fg="#0099CC")
        menu.add_cascade(label=idi["opcion"][z], menu=subMenu)
        subMenu.add_command(label=idi["menup"][z], command=lambda: self.mostrar_app("Main"))
        subMenu.add_separator()
        subMenu.add_command(label=idi["idioma"][z], command=self.cambiar_idioma)
        subMenu.add_command(label=idi["pcambio"][z], command=self.Cambio)
        subMenu.add_separator()
        subMenu.add_command(label=idi["descansa"][z], command=lambda: self.mostrar_app("Descansador"))
        subMenu.add_command(label=idi["apagar"][z], command=self.apagar)

        self.clases = [Main, AhorcadoUI, ContactosUI, AgendaUI, CalculadoraUI, Descansador]

        self.apps = {}

        self.last_app = "Main"

        self.cargar_apps(0)

        self.mostrar_app("Main")

    def cargar_apps(self, i):
        """
        :param i:
        Carga cada Frame dentro del dict apps
        """
        if i < len(self.clases):
            nombre = self.clases[i].__name__
            app = self.clases[i](master=self.root, controlador=self)
            self.apps[nombre] = app
            app.place(relwidth=1, relheight=1)

            self.cargar_apps(i + 1)

    def mostrar_app(self, nombre):
        """
        :param nombre: str, nombre de la app que se quiere mostrar en la interfaz.
        Alza la frame que sea desea mostrar por encima del resto.
        """
        if nombre != "Descansador":
            self.last_app = nombre
        app = self.apps[nombre]
        app.tkraise()

    def guardazilla(self):
        global z
        WatchOs.set_idioma(idioma=z)
        self.apps["ContactosUI"].contactos.save()
        self.apps["AgendaUI"].actividades.save()

    def apagar(self):
        """
        Llama las funciones que se encargan de guardar los datos y apagar el sistema.
        """
        self.guardazilla()
        self.root.destroy()
        Comienzo()

    def cambiar_idioma(self):
        """
        Cambia el idioma de la interfaz -Provoca que la ventana se cierre y abra para hacer el cambio-
        """
        global z
        if z:
            z = 0
        else:
            z = 1
        self.guardazilla()
        self.root.destroy()
        Controlador()

    class Cambio:
        def __init__(self):
            """
            Provee una interfaz para que el usuario cambie el pin del dispositivo
            """
            self.root = tk.Tk()
            self.root.title(string=idi["pcambio"][z])
            self.root.geometry("280x100+500+200")
            self.root.iconbitmap(bitmap="imagenes/watch.ico")
            self.root.config(bg="#212121")
            self.pin = tk.StringVar(self.root)
            self.instruc = tk.Label(master=self.root, text=idi["npin"][z], bg="#212121", fg="#ffffff")
            self.instruc.place(x=72, y=5)
            self.nuevo = tk.Entry(master=self.root, textvariable=self.pin)
            self.nuevo.place(x=75, y=30)
            self.nuevo.bind("<Return>", func=self.cambiar_pin)
            self.resultado = tk.Label(self.root, bg="#212121")

        def cambiar_pin(self, *args):
            """
            :param args:
            :Restricciones Debe ser un int y estar entre el rango de ]0,9999]
            Cambia el pin de acceso en disco.
            """
            if WatchOs.cambiar_pin(self.pin.get()):
                self.resultado.config(text=idi["cepin"][z], fg="#4285F4")
                self.resultado.place(x=35, y=60)
            else:
                self.resultado.config(text=idi["cfpin"][z], fg="#ffbb33")
                self.resultado.place(x=10, y=60)


class Main(tk.Frame):
    """
    Interfaz principal del reloj inteligente
    """

    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.controlador = controlador

        # Fondo de pantalla
        fondo = Image.open("imagenes/background.png")
        fondo = fondo.resize((600, 500), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(fondo)
        self.background = tk.Label(self, image=test)
        self.background.image = test
        self.background.place(relwidth=1, relheight=1)

        # Botón hacia contactos
        image1 = Image.open("imagenes/contactos.png")
        image1 = image1.resize((50, 50), Image.ANTIALIAS)
        self.conticon = ImageTk.PhotoImage(image1)

        self.contacts = tk.Button(self, command=lambda: self.controlador.mostrar_app("ContactosUI"), bg="#AF9483",
                                  borderwidth=0)
        self.contacts.place(x=75, y=325)
        self.contacts.config(image=self.conticon)

        # Botón hacia agenda
        image2 = Image.open("imagenes/agenda.png")
        image2 = image2.resize((50, 50), Image.ANTIALIAS)
        self.agenicon = ImageTk.PhotoImage(image2)

        self.agenda = tk.Button(self, command=lambda: self.controlador.mostrar_app("AgendaUI"), bg="#AF9483",
                                borderwidth=0)
        self.agenda.place(x=200, y=325)
        self.agenda.config(image=self.agenicon)

        # Botón hace calculadora
        image3 = Image.open("imagenes/calculadora.png")
        image3 = image3.resize((50, 50), Image.ANTIALIAS)
        self.calcicon = ImageTk.PhotoImage(image3)

        self.calculadora = tk.Button(self, command=lambda: self.controlador.mostrar_app("CalculadoraUI"), bg="#AF9483",
                                     borderwidth=0)
        self.calculadora.place(x=325, y=325)
        self.calculadora.config(image=self.calcicon)

        # Botón hacia ahorcado
        image4 = Image.open("imagenes/ahorcado.png")
        image4 = image4.resize((50, 50), Image.ANTIALIAS)
        self.ahorcicon = ImageTk.PhotoImage(image4)

        self.ahorcado = tk.Button(self, command=lambda: self.controlador.mostrar_app("AhorcadoUI"), bg="#AF9483",
                                  borderwidth=0)
        self.ahorcado.place(x=450, y=325)
        self.ahorcado.config(image=self.ahorcicon)

        # Genera label que representa el reloj
        ahora = WatchOs.get_time()
        self.reloj = tk.Label(master=self, text=f"{ahora.hour}:{ahora.minute}:{ahora.second}",
                              font=("Roboto", 40), bg="#AD5D5D", fg="#ffffff")

        # Genera label que representa la fecha
        self.fecha = tk.Label(master=self, text=WatchOs.get_date(),
                              font=("Roboto", 15), bg="#AD5D5D", fg="#ffffff")

        self.reloj.place(x=200, y=100)
        self.fecha.place(x=223, y=160)

        self.actualizar_hora()
        self.actualizar_fecha()

    def actualizar_hora(self):
        """
        Actualiza el reloj por segundo.
        """
        ahora = WatchOs.get_time()
        self.reloj.config(text=f"{ahora.hour}:{ahora.minute}:{ahora.second}")

        self.reloj.after(ms=1000, func=lambda: self.actualizar_hora())

    def actualizar_fecha(self):
        """
        Actualiza la fecha por minuto.
        """
        self.fecha.config(text=WatchOs.get_date())

        self.fecha.after(ms=60000, func=lambda: self.actualizar_fecha())


class AhorcadoUI(tk.Frame):
    """
    Interfaz para el juego de ahorcado
    """

    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.config(bg="#212121")
        self.controlador = controlador
        self.juego = WatchOs.Ahorcado(idi=z)

        self.palabra = self.juego.get_actual()

        self.ganadas = WatchOs.ganadas
        self.ganadaslabel = tk.Label(self, text=idi["ganadas"][z], font=("Roboto", 12), fg="#9933CC", bg="#212121")
        if not z:
            self.ganadaslabel.place(x=360, y=20)
        else:
            self.ganadaslabel.place(x=392, y=20)

        self.mostrar_ganadas = tk.Label(self, text=self.ganadas, font=("Roboto", 12), fg="#9933CC", bg="#212121")
        self.mostrar_ganadas.place(x=500, y=20)

        self.intentos = tk.IntVar()
        self.intentos.set(value=self.juego.intentos)

        self.pedido = tk.Label(self, text=idi["letra"][z], font=("Roboto", 12), fg="#2BBBAD", bg="#212121")
        self.pedido.place(x=218, y=240)

        self.restantes = tk.Label(self, text=idi["restantes"][z], font=("Roboto", 12), bg="#212121", fg="#0099CC")
        self.restantes.place(x=50, y=20)

        self.mostrar_intentos = tk.Label(self, textvariable=self.intentos, font=("Roboto", 12), bg="#212121",
                                         fg="#0099CC")
        if not z:
            self.mostrar_intentos.place(x=190, y=20)
        else:
            self.mostrar_intentos.place(x=150, y=20)

        self.guarda_letra = tk.StringVar()
        self.entrada = tk.Entry(self, textvariable=self.guarda_letra, bg="#263238", fg="#ffffff", borderwidth=0)
        self.entrada.bind("<Return>", func=self.comprueba)
        self.entrada.place(x=220, y=270)

        self.feedback = tk.StringVar()
        self.feedback_container = tk.Label(self, textvariable=self.feedback, font=("Roboto", 12), bg="#212121",
                                           fg="#ffbb33")
        self.feedback_container.place(x=220, y=300)

        self.secretas = self.adivina_labels(0, 125, [])

    def adivina_labels(self, i, coord, result):
        """
        :param i: int, índice
        :param coord: coordenada x donde se posiciona la label
        :param result: lista de Labels
        :return: result
        Crea labels que representan una incógnita de una letra según la cantidad de letras que la palabra actual
        posea.
        """
        if i >= len(self.palabra):
            return result
        else:
            result += [tk.Label(self, text="__", font=("Roboto", 20), fg="#ff4444", bg="#212121")]
            result[i].place(x=coord, y=150)
            return self.adivina_labels(i + 1, coord + 50, result)

    def eliminar_secretas(self, i):
        if i < len(self.secretas):
            self.secretas[i].destroy()
            self.eliminar_secretas(i + 1)

    def comprueba(self, *args):
        """
        :param args:
        :return: Determina si la letra adivinada por el usuario se encuentra en la palabra, no lo está,
        tiene longitud inválida o ya se adivino previamente.
        """
        letra = self.juego.comprobar_letra(self.guarda_letra.get())

        if letra == 1:
            self.mostrar(self.guarda_letra.get())
            self.feedback.set(idi["badivina"][z])

            if self.juego.comprobar_palabra():
                WatchOs.ganadas += 1
                self.terminar(True)

        elif letra == 0:
            self.feedback.set(idi["noletra"][z])

        elif letra == -1:
            self.intentos.set(self.intentos.get() - 1)
            self.feedback.set(idi["madivina"][z])
            if self.intentos.get() <= 3:
                self.mostrar_intentos.config(fg="#ffbb33")
            if not self.intentos.get():
                self.terminar(False)

        else:
            self.feedback.set(idi["readivina"][z])

    def mostrar(self, letra):
        """
        :param letra:
        :return: Al adivinar una letra, cambia las posiciones escondidas por la letra correspondiente
        """
        pos = self.juego.pos(letra, 0, [])
        self.mostrar_aux(pos, letra, 0)

    def mostrar_aux(self, pos, letra, i):
        if i < len(pos):
            self.secretas[pos[i]].config(text=letra)
            self.mostrar_aux(pos, letra, i + 1)

    def terminar(self, resultado):
        """
        Termina el juego en el caso que el jugador pierda o gane. Y le indica el resultado
        """
        final = tk.Frame(self)
        final.place(relwidth=1, relheight=1)
        if resultado:
            final.config(bg="#212121")
            ganador = tk.Label(master=final, text=idi["aganador"][z], font=("Roboto", 23), fg="#00C851", bg="#212121")
            ganador.place(relx=0.5, rely=0.5, anchor="center")

        else:
            final.config(bg="#212121")
            perdedor = tk.Label(master=final, text=idi["aperdedor"][z], font=("Roboto", 23), fg="#ff4444", bg="#212121")
            perdedor.place(relx=0.5, rely=0.5, anchor="center")

        reiniciar = tk.Button(master=final, text=idi["greiniciar"][z], command=lambda: self.reiniciar(final),
                              bg="#212121", fg="#0099CC", borderwidth=0)
        reiniciar.place(x=255, y=300)

    def reiniciar(self, garbage):
        garbage.destroy()
        self.juego.salvar()
        self.feedback_container.destroy()
        self.eliminar_secretas(0)

        self.juego = WatchOs.Ahorcado(idi=z)

        self.palabra = self.juego.get_actual()

        self.ganadas = WatchOs.ganadas
        self.ganadaslabel = tk.Label(self, text=idi["ganadas"][z], font=("Roboto", 12), fg="#9933CC", bg="#212121")
        self.ganadaslabel.place(x=360, y=20)

        self.mostrar_ganadas = tk.Label(self, text=self.ganadas, font=("Roboto", 12), fg="#9933CC", bg="#212121")
        self.mostrar_ganadas.place(x=500, y=20)

        self.intentos = tk.IntVar()
        self.intentos.set(value=self.juego.intentos)

        self.pedido = tk.Label(self, text=idi["letra"][z], font=("Roboto", 12), fg="#2BBBAD", bg="#212121")
        self.pedido.place(x=218, y=240)

        self.restantes = tk.Label(self, text=idi["restantes"][z], font=("Roboto", 12), bg="#212121", fg="#0099CC")
        self.restantes.place(x=50, y=20)

        self.mostrar_intentos = tk.Label(self, textvariable=self.intentos, font=("Roboto", 12), bg="#212121",
                                         fg="#0099CC")
        if not z:
            self.mostrar_intentos.place(x=190, y=20)
        else:
            self.mostrar_intentos.place(x=150, y=20)

        self.guarda_letra = tk.StringVar()
        self.entrada = tk.Entry(self, textvariable=self.guarda_letra, bg="#263238", fg="#ffffff", borderwidth=0)
        self.entrada.bind("<Return>", func=self.comprueba)
        self.entrada.place(x=220, y=270)

        self.feedback = tk.StringVar()
        self.feedback_container = tk.Label(self, textvariable=self.feedback, font=("Roboto", 12), bg="#212121",
                                           fg="#ffbb33")
        self.feedback_container.place(x=220, y=300)

        self.secretas = self.adivina_labels(0, 125, [])


class ContactosUI(tk.Frame):
    """
    Interfaz para mostrar contactos
    """

    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.config(bg="#212121")

        self.controlador = controlador
        self.contactos = WatchOs.Contactos()

        self.oid = tk.Button(self, text=f"{idi['oabc'][z]}", bg="#212121", fg="#00C851", borderwidth=0,
                             font=("Roboto", 11), command=lambda: self.ordenar_abc())
        self.oid.place(x=30, y=45)
        self.oabc = tk.Button(self, text=f"{idi['oid'][z]}", bg="#212121", fg="#00C851", borderwidth=0,
                              font=("Roboto", 11), command=lambda: self.ordenar_id())
        self.oabc.place(x=30, y=105)

        self.elegir = tk.Button(self, text=idi["idselect"][z], bg="#212121", fg="#00C851", borderwidth=0,
                                font=("Roboto", 11), command=lambda: self.seleccionar())
        self.elegir.place(x=30, y=165)

        self.agregar = tk.Button(self, text=idi["cagregar"][z], bg="#212121", fg="#00C851", borderwidth=0,
                                 font=("Roboto", 11), command=lambda: self.crear())
        self.agregar.place(x=30, y=250)

        self.botones = [None]

        self.cabeza = tk.Label(self, text=f"ID   {idi['contnombre'][z]}   {idi['conttel'][z]}   {idi['contcel'][z]}"
                                          f"   {idi['contcorreo'][z]}   {idi['contfoto'][z]}",
                               font=("Roboto", 12), bg="#212121", fg="#0099CC")

        self.labels = self.display(0, [self.cabeza])

        self.mostrar(0, 20, self.labels)

    def crear(self):
        nombre = tk.StringVar()
        nombre1 = tk.Label(self, text=idi["nombre"][z], bg="#212121", fg="#ffffff")
        nombre1.place(x=15, y=280)
        nombre2 = tk.Entry(self, textvariable=nombre, bg="#212121", fg="#ffffff")
        nombre2.place(x=70, y=280)

        tel = tk.StringVar()
        tel1 = tk.Label(self, text="Tel", bg="#212121", fg="#ffffff")
        tel1.place(x=15, y=305)
        tel2 = tk.Entry(self, textvariable=tel, bg="#212121", fg="#ffffff")
        tel2.place(x=70, y=305)

        cel = tk.StringVar()
        cel1 = tk.Label(self, text="Cel", bg="#212121", fg="#ffffff")
        cel1.place(x=15, y=330)
        cel2 = tk.Entry(self, textvariable=cel, bg="#212121", fg="#ffffff")
        cel2.place(x=70, y=330)

        correo = tk.StringVar()
        correo1 = tk.Label(self, text=idi["correo"][z], bg="#212121", fg="#ffffff")
        correo1.place(x=15, y=355)
        correo2 = tk.Entry(self, textvariable=correo, bg="#212121", fg="#ffffff")
        correo2.place(x=70, y=355)

        foto = tk.StringVar()
        foto1 = tk.Label(self, text=idi["foto"][z], bg="#212121", fg="#ffffff")
        foto1.place(x=15, y=380)
        foto2 = tk.Entry(self, textvariable=foto, bg="#212121", fg="#ffffff")
        foto2.place(x=70, y=380)

        enviar = tk.Button(self, text=idi["agregar"][z],
                           command=lambda: self.agregar_contacto(nombre.get(), tel.get(), cel.get(),
                                                                 correo.get(), foto.get()),
                           bg="#212121", fg="#ffffff")

        enviar.place(x=90, y=410)

    def agregar_contacto(self, nombre, tel, cel, correo, foto):
        if nombre is not None and tel is not None and cel is not None and correo is not None and foto is not None:
            self.contactos.crear(nombre=nombre, telefonos=tel, celular=cel, correo=correo, foto=foto)
            self.destruir(0)
            self.botones = [None]
            self.labels = self.display(0, [tk.Label(self, text=f"ID   {idi['contnombre'][z]}   {idi['conttel'][z]}"
                                                               f"   {idi['contcel'][z]}   {idi['contcorreo'][z]}"
                                                               f"   {idi['contfoto'][z]}",
                                                    font=("Roboto", 12), bg="#212121", fg="#0099CC")])
            self.mostrar(0, 20, self.labels)

    def ordenar_abc(self):
        """
        Ordena los contactos por su identificación
        """
        self.destruir(i=1)
        self.botones = [None]
        self.labels = self.display(i=0, result=[tk.Label(self, text=f"ID   {idi['contnombre'][z]}   {idi['conttel'][z]}"
                                                                    f"   {idi['contcel'][z]}   {idi['contcorreo'][z]}"
                                                                    f"   {idi['contfoto'][z]}",
                                                         font=("Roboto", 12), bg="#212121", fg="#0099CC")],
                                   modo=self.contactos.ordenar_abc())
        self.mostrar(i=0, j=20, labels=self.labels)

    def ordenar_id(self):
        """
        :return: Ordena los contactos por id
        """
        self.destruir(i=1)
        self.botones = [None]
        self.labels = self.display(i=0, result=[tk.Label(self, text=f"ID   {idi['contnombre'][z]}   {idi['conttel'][z]}"
                                                                    f"   {idi['contcel'][z]}   {idi['contcorreo'][z]}"
                                                                    f"   {idi['contfoto'][z]}",
                                                         font=("Roboto", 12), bg="#212121", fg="#0099CC")],
                                   modo=self.contactos.ordenar_id())
        self.mostrar(i=0, j=20, labels=self.labels)

    def seleccionar(self):
        """
        Provee entry para poder seleccionar un solo contacto
        """
        cual1 = tk.Label(self, text="ID:", bg="#212121", fg="#ba68c8", font=("Roboto", 10))
        cual1.place(x=20, y=200)
        identidad = tk.IntVar()
        cual2 = tk.Entry(self, textvariable=identidad, bg="#00695c", fg="#ffffff", borderwidth=0, font=("Roboto", 10))
        cual2.bind(sequence="<Return>", func=lambda x: self.escoger(identidad.get(), cual1, cual2))
        cual2.place(x=45, y=200)

    def escoger(self, identidad, label, entry):
        """
        :param identidad: identidad del contacto que se escogió
        :param label: label de seleccionar para borrar
        :param entry: entry de seleccionar para borrar
        Al escojer un usuario lo aisla y muestra
        """
        if isinstance(identidad, int) and identidad < len(self.contactos.contacts):
            label.destroy()
            entry.destroy()
            self.destruir(0)
            cont = self.contactos.contacts[identidad]
            seleccionado1 = tk.Label(self, text=f"{cont.identidad}   {cont.nombre}   "
                                                f"{cont.telefonos}   {cont.celular}   {cont.correo}   "
                                                f"{cont.foto}", font=("Roboto", 10), bg="#212121", fg="#ffffff")
            seleccionado1.place(x=220, y=30)

            seleccionado2 = tk.Button(self, text=f"{idi['delcont'][z]}", command=lambda: self.eliminar(identidad),
                                      font=("Roboto", 8), bg="#212121", fg="#ff4444", borderwidth=0)

            seleccionado2.place(x=220, y=60)

    def display(self, i, result, modo=None):
        """
        :param abc: lista, contactos ordenados por el abecedario. -opcional-
        :param i:
        :param result:
        :return: llena listas con las widgets necesarias para mostrar.
        """
        if not modo:
            conts = self.contactos.contacts
        else:
            conts = modo
        if i < len(conts):
            result += [tk.Label(self, text=f"{conts[i].identidad}   {conts[i].nombre}   "
                                           f"{conts[i].telefonos}   {conts[i].celular}   {conts[i].correo}   "
                                           f"{conts[i].foto}", font=("Roboto", 10), bg="#212121", fg="#ffffff")]

            self.botones += [
                tk.Button(self, text=f"{idi['delcont'][z]}", command=lambda: self.eliminar(i),
                          font=("Roboto", 8), bg="#212121", fg="#ff4444", borderwidth=0)]

            return self.display(i=i + 1, result=result, modo=modo)
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
            labels[i].place(x=220, y=j)
            self.botones[i].place(x=220, y=j + 30)
            self.mostrar(i + 1, j + 70, labels)
        elif i < len(labels):
            labels[i].place(x=220, y=j)
            self.mostrar(i + 1, j + 30, labels)

    def eliminar(self, i):
        """
        :param i: int, identidad del contacto a eliminar
        Elimina un solo usuario y se encarga de cargar de nuevo los conactos
        """
        self.contactos.eliminar(i)
        self.destruir(0)
        self.botones = [None]
        self.labels = self.display(0, [tk.Label(self, text=f"ID   {idi['contnombre'][z]}   {idi['conttel'][z]}"
                                                           f"   {idi['contcel'][z]}   {idi['contcorreo'][z]}"
                                                           f"   {idi['contfoto'][z]}",
                                                font=("Roboto", 12), bg="#212121", fg="#0099CC")])
        self.mostrar(0, 20, self.labels)

    def destruir(self, i):
        if i < len(self.labels):
            self.labels[i].destroy()
            if i != 0 and i < len(self.botones):
                self.botones[i].destroy()
            self.destruir(i + 1)


class AgendaUI(tk.Frame):
    """
    Interfaz para mostrar agenda
    """

    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.config(bg="#212121")

        self.controlador = controlador
        self.actividades = WatchOs.Agenda()

        self.regresar = None

        self.fecha = tk.Button(self, text=idi["amostrar"][z], bg="#212121", fg="#00C851", borderwidth=0,
                               font=("Roboto", 11), command=lambda: self.seleccionar())

        self.fecha.place(x=30, y=80)

        self.incluir = tk.Button(self, text=idi["aincluir"][z], bg="#212121", fg="#00C851", borderwidth=0,
                                 font=("Roboto", 11), command=lambda: self.crear())

        self.incluir.place(x=30, y=160)

        self.bot_eliminar = [None]

        self.bot_fecha = [None]

        self.bot_hora = [None]

        self.labels = self.display(0, [tk.Label(self,
                                                text=f"ID   {idi['agenfecha'][z]}   {idi['agenhora'][z]}   "
                                                     f"{idi['agenevento'][z]}", font=("Roboto", 12),
                                                bg="#212121", fg="#4285F4")], labels=self.actividades.agenda)

        self.mostrar(i=0, j=20, labels=self.labels)

    def crear(self):
        evento = tk.StringVar()
        evento1 = tk.Label(self, text=idi["agenevento"][z], bg="#212121", fg="#ffffff")
        evento1.place(x=15, y=200)
        evento2 = tk.Entry(self, textvariable=evento, bg="#212121", fg="#ffffff")
        evento2.place(x=60, y=200)

        fecha = tk.StringVar()
        fecha1 = tk.Label(self, text=idi["agenfecha"][z], bg="#212121", fg="#ffffff")
        fecha1.place(x=15, y=240)
        fecha2 = tk.Entry(self, textvariable=fecha, bg="#212121", fg="#ffffff")
        fecha2.place(x=60, y=240)

        tiempo = tk.StringVar()
        tiempo1 = tk.Label(self, text=idi["agenhora"][z], bg="#212121", fg="#ffffff")
        tiempo1.place(x=15, y=280)
        tiempo2 = tk.Entry(self, textvariable=tiempo, bg="#212121", fg="#ffffff")
        tiempo2.place(x=60, y=280)

        enviar = tk.Button(self, text=idi["agregar"][z],
                           command=lambda: self.agregar_evento(fecha.get(), tiempo.get(), evento.get()),
                           bg="#212121", fg="#ffffff")

        enviar.place(x=90, y=320)

    def eliminar(self, i):
        """
        :param i: int, identidad del contacto a eliminar
        Elimina un solo usuario y se encarga de cargar de nuevo los conactos
        """
        self.actividades.eliminar(i)
        self.destruir(0)
        self.bot_eliminar = [None]
        self.bot_fecha = [None]
        self.bot_hora = [None]

        self.labels = self.display(0, [tk.Label(self,
                                                text=f"ID   {idi['agenfecha'][z]}   {idi['agenhora'][z]}   "
                                                     f"{idi['agenevento'][z]}", font=("Roboto", 12),
                                                bg="#212121", fg="#4285F4")], labels=self.actividades.agenda)
        self.mostrar(0, 20, self.labels)

    def regreso(self):

        self.bot_eliminar = [None]

        self.bot_fecha = [None]

        self.bot_hora = [None]

        self.labels = self.display(0, [tk.Label(self,
                                                text=f"ID   {idi['agenfecha'][z]}   {idi['agenhora'][z]}   "
                                                     f"{idi['agenevento'][z]}", font=("Roboto", 12),
                                                bg="#212121", fg="#4285F4")], labels=self.actividades.agenda)

        self.mostrar(i=0, j=20, labels=self.labels)

    def agregar_evento(self, fecha, hora, evento):
        if fecha is not None and hora is not None and evento is not None:
            self.actividades.incluir(fecha=fecha, hora=hora, info=evento)
            self.destruir(0)
            self.bot_eliminar = [None]
            self.bot_fecha = [None]
            self.bot_hora = [None]

            self.labels = self.display(0, [tk.Label(self, text=f"ID   {idi['agenfecha'][z]}   {idi['agenhora'][z]}   "
                                                               f"{idi['agenevento'][z]}", font=("Roboto", 12),
                                                    bg="#212121", fg="#4285F4")], labels=self.actividades.agenda)
            self.mostrar(0, 20, self.labels)

    def seleccionar(self):
        """
        Provee entry para poder seleccionar una sola actividad
        """
        cual1 = tk.Label(self, text="ID", bg="#212121", fg="#ffffff", font=("Roboto", 10))
        cual1.place(x=20, y=110)
        fecha = tk.StringVar()
        cual2 = tk.Entry(self, textvariable=fecha, bg="#212121", fg="#ffffff", font=("Roboto", 10))
        cual2.bind(sequence="<Return>", func=lambda x: self.escoger(fecha.get(), cual1, cual2))
        cual2.place(x=45, y=111)

    def escoger(self, fecha, label, entry):
        """
        :param identidad: identidad del contacto que se escogió
        :param label: label de seleccionar para borrar
        :param entry: entry de seleccionar para borrar
        Al escojer una actividad la aisla y muestra
        """
        actv = self.get_actv(i=0, fecha=fecha, result=[])
        if actv:
            label.destroy()
            entry.destroy()
            self.destruir(0)
            self.bot_fecha = [None]
            self.bot_eliminar = [None]
            self.bot_hora = [None]
            actv_labels = self.display(i=0, result=[tk.Label(self, text=f"ID   {idi['agenfecha'][z]}   {idi['agenhora'][z]}"
                                                                        f"   {idi['agenevento'][z]}", font=("Roboto", 12),
                                                             bg="#212121", fg="#4285F4")], labels=actv)
            self.mostrar(i=0, j=20, labels=actv_labels)

            self.regresar = tk.Button(self, text=idi["regresar"][z], bg="#212121", fg="#ff4444", font=("Roboto", 11),
                                      borderwidth=0, command=lambda: self.regreso())

            self.regresar.place(x=90, y=360)

    def get_actv(self, i, fecha, result):
        if i >= len(self.actividades.agenda):
            return result
        elif self.actividades.agenda[i].fecha == fecha:
            result += [self.actividades.agenda[i]]
            return self.get_actv(i+1, fecha, result)
        else:
            return self.get_actv(i+1, fecha, result)

    def cambiar_fecha(self, evento):
        self.labels[evento+1].destroy()
        diff_fecha = tk.StringVar()
        cambio = tk.Entry(self, textvariable=diff_fecha)
        cambio.bind(sequence="<Return>", func=lambda x: self.cambio_fecha(evento=evento, info=diff_fecha,
                                                                          garbage=cambio))
        cambio.insert(0, self.actividades.agenda[evento].fecha)
        cambio.place(x=300, y=70*(evento+1))

    def cambio_fecha(self, evento, info, garbage):
        garbage.destroy()
        actv = self.actividades.agenda
        actv[evento].fecha = info.get()
        self.labels[evento+1] = tk.Label(self, text=f"{actv[evento].identidad}   {actv[evento].fecha}"
                                                  f"   {actv[evento].hora}   {actv[evento].info}",
                                       font=("Roboto", 10),  bg="#212121", fg="#ffffff")
        self.labels[evento+1].place(x=220, y=70+(70*evento+1))

    def cambiar_hora(self, evento):
        self.labels[evento+1].destroy()
        diff_hora = tk.StringVar()
        cambio = tk.Entry(self, textvariable=diff_hora)
        cambio.bind(sequence="<Return>", func=lambda x: self.cambio_hora(evento=evento, info=diff_hora,
                                                                          garbage=cambio))
        cambio.insert(0, self.actividades.agenda[evento].hora)
        cambio.place(x=300, y=70*(evento+1))

    def cambio_hora(self, evento, info, garbage):
        garbage.destroy()
        actv = self.actividades.agenda
        actv[evento].hora = info.get()
        self.labels[evento+1] = tk.Label(self, text=f"{actv[evento].identidad}   {actv[evento].fecha}"
                                                  f"   {actv[evento].hora}   {actv[evento].info}",
                                       font=("Roboto", 10),  bg="#212121", fg="#ffffff")
        self.labels[evento+1].place(x=220, y=70+(70*evento+1))

    def display(self, i, result, labels):
        """
        :param fecha: lista de labels que de una sola fehca
        :param i: int
        :param result: lista de labels
        :return: result
        Crea una lista de Labels necesarias para sostener todas las habilidades guardadas.
        """
        if i < len(labels):
            result += [tk.Label(self, text=f"{labels[i].identidad}   {labels[i].fecha}   {labels[i].hora}   "
                                           f"{labels[i].info}", font=("Roboto", 10),  bg="#212121", fg="#ffffff")]

            self.bot_eliminar += [
                tk.Button(self, text=idi["adel"][z], command=lambda: self.eliminar(i=i),
                          font=("Roboto", 8), bg="#212121", fg="#ff4444", borderwidth=0)]

            self.bot_fecha += [
                tk.Button(self, text=idi["afecha"][z], command=lambda: self.cambiar_fecha(evento=i),
                          font=("Roboto", 8), bg="#212121", fg="#ff4444", borderwidth=0)]

            self.bot_hora += [
                tk.Button(self, text=idi["ahora"][z], command=lambda: self.cambiar_hora(evento=i),
                          font=("Roboto", 8), bg="#212121", fg="#ff4444", borderwidth=0)]

            return self.display(i + 1, result, labels)
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
            labels[i].place(x=220, y=j)
            self.bot_eliminar[i].place(x=220, y=j + 30)
            self.bot_fecha[i].place(x=310, y=j+30)
            self.bot_hora[i].place(x=400, y=j+30)
            self.mostrar(i + 1, j + 70, labels)
        elif i < len(labels):
            labels[i].place(x=220, y=j)
            self.mostrar(i + 1, j + 50, labels)

    def destruir(self, i):
        if i < len(self.labels):
            self.labels[i].destroy()
            if i != 0 and i < len(self.bot_eliminar):
                self.bot_eliminar[i].destroy()
                self.bot_fecha[i].destroy()
                self.bot_hora[i].destroy()
            self.destruir(i + 1)


class CalculadoraUI(tk.Frame):
    """
    Calculadora y sus operaciones
    - Modificada del código de Joshua León Czech -
    """
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.config(bg="#212121")
        self.controlador = controlador

        self.i = 0
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        self.columnconfigure(4, pad=3)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)

        self.display = tk.Entry(self, font=("Roboto", 30), bg="#212121", fg="#ffffff")
        self.display.grid(row=1, columnspan=10, sticky=tk.W + tk.E)

        one = tk.Button(self, text="1", command=lambda: self.get_variables(1), font=("Roboto", 42),
                        bg="#212121", fg="#0099CC", borderwidth=0)
        one.grid(row=2, column=0)
        two = tk.Button(self, text="2", command=lambda: self.get_variables(2), font=("Roboto", 42),
                        bg="#212121", fg="#0099CC", borderwidth=0)
        two.grid(row=2, column=1)
        three = tk.Button(self, text="3", command=lambda: self.get_variables(3), font=("Roboto", 42),
                          bg="#212121", fg="#0099CC", borderwidth=0)
        three.grid(row=2, column=2)

        four = tk.Button(self, text="4", command=lambda: self.get_variables(4), font=("Roboto", 42),
                         bg="#212121", fg="#0099CC", borderwidth=0)
        four.grid(row=3, column=0)
        five = tk.Button(self, text="5", command=lambda: self.get_variables(5), font=("Roboto", 42),
                         bg="#212121", fg="#0099CC", borderwidth=0)
        five.grid(row=3, column=1)
        six = tk.Button(self, text="6", command=lambda: self.get_variables(6), font=("Roboto", 42),
                        bg="#212121", fg="#0099CC", borderwidth=0)
        six.grid(row=3, column=2)

        seven = tk.Button(self, text="7", command=lambda: self.get_variables(7), font=("Roboto", 42),
                          bg="#212121", fg="#0099CC", borderwidth=0)
        seven.grid(row=4, column=0)
        eight = tk.Button(self, text="8", command=lambda: self.get_variables(8), font=("Roboto", 42),
                          bg="#212121", fg="#0099CC", borderwidth=0)
        eight.grid(row=4, column=1)
        nine = tk.Button(self, text="9", command=lambda: self.get_variables(9), font=("Roboto", 42),
                         bg="#212121", fg="#0099CC", borderwidth=0)
        nine.grid(row=4, column=2)

        cls = tk.Button(self, text="AC", command=self.clear_all, font=("Roboto", 42),
                        bg="#212121", fg="#ff4444", borderwidth=0)
        cls.grid(row=5, column=0)
        zero = tk.Button(self, text="0", command=lambda: self.get_variables(0), font=("Roboto", 42),
                         bg="#212121", fg="#0099CC", borderwidth=0)
        zero.grid(row=5, column=1)
        result = tk.Button(self, text="=", command=self.calculate, font=("Roboto", 42),
                           bg="#212121", fg="#ff4444", borderwidth=0)
        result.grid(row=5, column=2)
        plus = tk.Button(self, text="+", command=lambda: self.get_operation("+"), font=("Roboto", 42),
                         bg="#212121", fg="#00C851", borderwidth=0)
        plus.grid(row=2, column=3)
        minus = tk.Button(self, text="-", command=lambda: self.get_operation("-"), font=("Roboto", 42),
                          bg="#212121", fg="#00C851", borderwidth=0)
        minus.grid(row=3, column=3)
        multiply = tk.Button(self, text="*", command=lambda: self.get_operation("*"), font=("Roboto", 42),
                             bg="#212121", fg="#00C851", borderwidth=0)
        multiply.grid(row=4, column=3)
        divide = tk.Button(self, text="/", command=lambda: self.get_operation("/"), font=("Roboto", 42),
                           bg="#212121", fg="#00C851", borderwidth=0)
        divide.grid(row=5, column=3)

        pi = tk.Button(self, text="pi", command=lambda: self.get_operation("*3.14"), font=("Roboto", 42),
                       bg="#212121", fg="#ffbb33", borderwidth=0)
        pi.grid(row=2, column=4)
        modulo = tk.Button(self, text="%", command=lambda: self.get_operation("%"), font=("Roboto", 42),
                           bg="#212121", fg="#00C851", borderwidth=0)
        modulo.grid(row=3, column=4)
        left_bracket = tk.Button(self, text="(", command=lambda: self.get_operation("("), font=("Roboto", 42),
                                 bg="#212121", fg="#00C851", borderwidth=0)
        left_bracket.grid(row=4, column=4)
        exp = tk.Button(self, text="exp", command=lambda: self.get_operation("**"), font=("Roboto", 40),
                        bg="#212121", fg="#00C851", borderwidth=0)
        exp.grid(row=5, column=4)

        undo_button = tk.Button(self, text="<", command=self.undo, font=("Roboto", 42),
                                bg="#212121", fg="#ff4444", borderwidth=0)
        undo_button.grid(row=2, column=5)
        fact = tk.Button(self, text="x!", command=self.factorial, font=("Roboto", 42),
                         bg="#212121", fg="#00C851", borderwidth=0)
        fact.grid(row=3, column=5)
        right_bracket = tk.Button(self, text=")", command=lambda: self.get_operation(")"), font=("Roboto", 42),
                                  bg="#212121", fg="#00C851", borderwidth=0)
        right_bracket.grid(row=4, column=5)
        square = tk.Button(self, text="^2", command=lambda: self.get_operation("**2"), font=("Roboto", 40),
                           bg="#212121", fg="#00C851", borderwidth=0)
        square.grid(row=5, column=5)

    def factorial(self):
        # Calcula el factorial del numero ingresado
        whole_string = self.display.get()
        number = int(whole_string)
        fact = 1
        counter = number
        try:
            while counter > 0:
                fact = fact * counter
                counter -= 1
            self.clear_all()
            self.display.insert(0, fact)
        except Exception:
            self.clear_all()
            self.display.insert(0, "Error")

    def clear_all(self):
        # Quita cualquier cosa ingresada en la entry box
        self.display.delete(0, tk.END)

    def get_variables(self, num):
        # Obtiene los operandos que ingreso el usuario y los pone dentro de la entry widget
        self.display.insert(self.i, num)
        self.i += 1

    def get_operation(self, operator):
        # Obtiene el operando para operacion
        length = len(operator)
        self.display.insert(self.i, operator)
        self.i += length

    def undo(self):
        # Remueve el ultimo digito que se puso en el entry box
        whole_string = self.display.get()
        if len(whole_string):
            new_string = whole_string[:-1]
            self.clear_all()
            self.display.insert(0, new_string)
        else:
            self.clear_all()
            self.display.insert(0, "Error, press AC")

    def calculate(self):
        # Evalua la expresion y la calcula
        whole_string = self.display.get()
        try:
            formulae = parser.expr(whole_string).compile()
            result = eval(formulae)
            self.clear_all()
            self.display.insert(0, result)
        except Exception:
            self.clear_all()
            self.display.insert(0, "Error!")



class Descansador(tk.Frame):
    """
    Interfaz donde se muestra y reproduce la animación del descansador
    """
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.config(bg="#212121")
        self.controlador = controlador

        self.hilo = threading.Thread(target=self.reproducir())
        self.hilo.start()

    def reproducir(self):
        animacion = ImageLabel(master=self)
        animacion.bind(sequence="<Button-1>",
                            func=lambda x: self.controlador.mostrar_app(self.controlador.last_app))
        animacion.pack()
        animacion.load(im="animacion/descansador.gif")


class ImageLabel(tk.Label):
    """
    objeto que permite la reproducción de gifs
    Crédito: https://stackoverflow.com/questions/43770847/play-an-animated-gif-in-python-with-tkinter
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


if __name__ == "__main__":
    Comienzo()
