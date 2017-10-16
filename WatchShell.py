import WatchOs
import tkinter as tk
from PIL import ImageTk
from PIL import Image
import calendar

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
    "correo": ("Correo:", "Email:"),
    "foto": ("Foto:", "Photo:"),
    "agregar": ("Agregar", "Add")
}

# Variable que determina el idioma actual, 0 = español / 1 = inglés
k = 0


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
        login_info = tk.Label(self.root, text=idi["pin"][k], bg="#212121", fg="#ffffff")
        login_info.place(x=65, y=0)
        contrasena = tk.Entry(self.root, textvariable=self.intento)
        contrasena.place(x=65, y=30)
        contrasena.bind("<Return>", self.confirma)
        prender = tk.Button(self.root, text=idi["prender"][k], command=self.confirma, borderwidth=0,
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
            self.respuesta.set(idi["exito"][k])
            self.root.destroy()
            Controlador()
        else:
            self.respuesta.set(idi["fallo"][k])


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
        menu.add_cascade(label=idi["opcion"][k], menu=subMenu)
        subMenu.add_command(label=idi["menup"][k], command=lambda: self.mostrar_app("Main"))
        subMenu.add_separator()
        subMenu.add_command(label=idi["idioma"][k], command=self.cambiar_idioma)
        subMenu.add_command(label=idi["pcambio"][k], command=self.Cambio)
        subMenu.add_command(label=idi["apagar"][k], command=self.apagar)

        self.apps = {}

        self.clases = [Main, AhorcadoUI, ContactosUI, AgendaUI, CalculadoraUI]

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
        app = self.apps[nombre]
        app.tkraise()

    class Cambio:
        def __init__(self):
            """
            Provee una interfaz para que el usuario cambie el pin del dispositivo
            """
            self.root = tk.Tk()
            self.root.title(string=idi["pcambio"][k])
            self.root.geometry("250x75+500+200")
            self.root.iconbitmap(bitmap="imagenes/watch.ico")
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
        Cambia el idioma de la interfaz -Provoca que la ventana se cierre y abra para hacer el cambio-
        """
        global k
        if k:
            k = 0
        else:
            k = 1
        self.root.destroy()
        Controlador()


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
        self.fecha = tk.Label(master=self, text=f"{calendar.month_name[ahora.month]} {ahora.day}, {ahora.year}",
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
        ahora = WatchOs.get_time()
        self.fecha.config(text=f"{calendar.month_name[ahora.month]} {ahora.day}, {ahora.year}")

        self.fecha.after(ms=60000, func=lambda: self.actualizar_fecha())


class AhorcadoUI(tk.Frame):
    """
    Interfaz para el juego de ahorcado
    """

    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.config(bg="#212121")
        self.controlador = controlador
        self.juego = WatchOs.Ahorcado(idi=k)

        self.palabra = self.juego.get_actual()

        self.intentos = tk.IntVar()
        self.intentos.set(value=self.juego.intentos)

        self.pedido = tk.Label(self, text=idi["letra"][k], font=("Roboto", 12), fg="#2BBBAD", bg="#212121")
        self.pedido.place(x=218, y=240)

        self.restantes = tk.Label(self, text=idi["restantes"][k], font=("Roboto", 12), bg="#212121", fg="#0099CC")
        self.restantes.place(x=350, y=10)

        self.mostrar_intentos = tk.Label(self, textvariable=self.intentos, font=("Roboto", 12), bg="#212121",
                                         fg="#0099CC")
        if not k:
            self.mostrar_intentos.place(x=490, y=10)
        else:
            self.mostrar_intentos.place(x=450, y=10)

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
            self.feedback.set(idi["badivina"][k])

            if self.juego.comprobar_palabra():
                self.terminar(True)

        elif letra == 0:
            self.feedback.set(idi["noletra"][k])

        elif letra == -1:
            self.intentos.set(self.intentos.get() - 1)
            self.feedback.set(idi["madivina"][k])
            if self.intentos.get() <= 3:
                self.mostrar_intentos.config(fg="#ffbb33")
            if not self.intentos.get():
                self.terminar(False)

        else:
            self.feedback.set(idi["readivina"][k])

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
            ganador = tk.Label(master=final, text=idi["aganador"][k], font=("Roboto", 23), fg="#00C851", bg="#212121")
            ganador.place(relx=0.5, rely=0.5, anchor="center")

        else:
            final.config(bg="#212121")
            perdedor = tk.Label(master=final, text=idi["aperdedor"][k], font=("Roboto", 23), fg="#ff4444", bg="#212121")
            perdedor.place(relx=0.5, rely=0.5, anchor="center")

        reiniciar = tk.Button(master=final, text=idi["greiniciar"][k], command=lambda: self.reiniciar(final),
                              bg="#212121", fg="#0099CC", borderwidth=0)
        reiniciar.place(x=255, y=300)

    def reiniciar(self, garbage):
        garbage.destroy()
        self.feedback_container.destroy()
        self.eliminar_secretas(0)

        self.juego = WatchOs.Ahorcado(idi=k)

        self.palabra = self.juego.get_actual()

        self.intentos = tk.IntVar()
        self.intentos.set(value=self.juego.intentos)

        self.pedido = tk.Label(self, text=idi["letra"][k], font=("Roboto", 12), fg="#2BBBAD", bg="#212121")
        self.pedido.place(x=221, y=240)

        self.restantes = tk.Label(self, text=idi["restantes"][k], font=("Roboto", 12), bg="#212121", fg="#0099CC")
        self.restantes.place(x=350, y=10)

        self.mostrar_intentos = tk.Label(self, textvariable=self.intentos, font=("Roboto", 12), bg="#212121",
                                         fg="#0099CC")
        if not k:
            self.mostrar_intentos.place(x=490, y=10)
        else:
            self.mostrar_intentos.place(x=450, y=10)

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

        self.oid = tk.Button(self, text=f"{idi['oabc'][k]}", bg="#212121", fg="#00C851", borderwidth=0,
                             font=("Roboto", 10), command=lambda: self.ordenar_abc())
        self.oid.place(x=30, y=45)
        self.oabc = tk.Button(self, text=f"{idi['oid'][k]}", bg="#212121", fg="#00C851", borderwidth=0,
                              font=("Roboto", 10), command=lambda: self.ordenar_abc())
        self.oabc.place(x=30, y=105)

        self.elegir = tk.Button(self, text=idi["idselect"][k], bg="#212121", fg="#00C851", borderwidth=0,
                                font=("Roboto", 10), command=lambda: self.seleccionar())
        self.elegir.place(x=30, y=165)

        self.agregar = tk.Button(self, text=idi["cagregar"][k], bg="#212121", fg="#00C851", borderwidth=0,
                                 font=("Roboto", 10), command=lambda: self.crear())
        self.agregar.place(x=30, y=250)

        self.botones = [None]

        self.cabeza = tk.Label(self, text=f"ID   {idi['contnombre'][k]}   {idi['conttel'][k]}   {idi['contcel'][k]}"
                                          f"   {idi['contcorreo'][k]}   {idi['contfoto'][k]}",
                               font=("Roboto", 10), bg="#212121", fg="#0099CC")

        self.labels = self.display(0, [self.cabeza])

        self.mostrar(0, 0, self.labels)

    def crear(self):
        nombre = tk.StringVar()
        nombre1 = tk.Label(self, text="ID:", bg="#212121", fg="#8e24aa")
        nombre1.place(x=20, y=280)
        nombre2 = tk.Entry(self, textvariable=nombre, bg="#212121", fg="#ffffff")
        nombre2.place(x=65, y=280)

        tel = tk.StringVar()
        tel1 = tk.Label(self, text="Tel:", bg="#212121", fg="#8e24aa")
        tel1.place(x=20, y=305)
        tel2 = tk.Entry(self, textvariable=tel, bg="#212121", fg="#ffffff")
        tel2.place(x=65, y=305)

        cel = tk.StringVar()
        cel1 = tk.Label(self, text="Cel:", bg="#212121", fg="#8e24aa")
        cel1.place(x=20, y=330)
        cel2 = tk.Entry(self, textvariable=cel, bg="#212121", fg="#ffffff")
        cel2.place(x=65, y=330)

        correo = tk.StringVar()
        correo1 = tk.Label(self, text=idi["correo"][k], bg="#212121", fg="#8e24aa")
        correo1.place(x=20, y=355)
        correo2 = tk.Entry(self, textvariable=correo, bg="#212121", fg="#ffffff")
        correo2.place(x=65, y=355)

        foto = tk.StringVar()
        foto1 = tk.Label(self, text=idi["foto"][k], bg="#212121", fg="#8e24aa")
        foto1.place(x=20, y=380)
        foto2 = tk.Entry(self, textvariable=foto, bg="#212121", fg="#ffffff")
        foto2.place(x=65, y=380)

        enviar = tk.Button(self, text=idi["agregar"][k],
                           command=lambda: self.agregar_contacto(nombre.get(), tel.get(), cel.get(),
                                                                 correo.get(), foto.get()),
                           bg="#212121", fg="#ffffff")

        enviar.place(x=90, y=410)

    def agregar_contacto(self, nombre, tel, cel, correo, foto):
        if nombre is not None and tel is not None and cel is not None and correo is not None and foto is not None:
            self.contactos.crear(nombre=nombre, telefonos=tel, celular=cel, correo=correo, foto=foto)
            self.destruir(0)
            self.botones = [None]
            self.labels = self.display(0, [tk.Label(self, text=f"ID   {idi['contnombre'][k]}   {idi['conttel'][k]}"
                                                               f"   {idi['contcel'][k]}   {idi['contcorreo'][k]}"
                                                               f"   {idi['contfoto'][k]}",
                                                    font=("Roboto", 10), bg="#212121", fg="#0099CC")])
            self.mostrar(0, 0, self.labels)

    def ordenar_abc(self):
        # TODO
        """
        Ordena los contactos por su identificación
        """
        self.destruir(0)
        self.botones = [None]
        self.labels = self.display(0, [tk.Label(self, text=f"ID   {idi['contnombre'][k]}   {idi['conttel'][k]}"
                                                           f"   {idi['contcel'][k]}   {idi['contcorreo'][k]}"
                                                           f"   {idi['contfoto'][k]}",
                                                font=("Roboto", 10), bg="#212121", fg="#0099CC")],
                                   abc=self.contactos.ordenar_abc())
        self.mostrar(0, 0, self.labels)

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

            seleccionado2 = tk.Button(self, text=f"{idi['delcont'][k]}", command=lambda: self.eliminar(identidad),
                                      font=("Roboto", 8), bg="#212121", fg="#ff4444", borderwidth=0)

            seleccionado2.place(x=220, y=60)

    def display(self, i, result, abc=None):
        """
        :param abc: lista, contactos ordenados por el abecedario. -opcional-
        :param i:
        :param result:
        :return: llena listas con las widgets necesarias para mostrar.
        """
        if not abc:
            conts = self.contactos.contacts
        else:
            conts = abc
        if i < len(conts):
            result += [tk.Label(self, text=f"{conts[i].identidad}   {conts[i].nombre}   "
                                           f"{conts[i].telefonos}   {conts[i].celular}   {conts[i].correo}   "
                                           f"{conts[i].foto}", font=("Roboto", 10), bg="#212121", fg="#ffffff")]

            self.botones += [
                tk.Button(self, text=f"{idi['delcont'][k]}", command=lambda: self.eliminar(i),
                          font=("Roboto", 8), bg="#212121", fg="#ff4444", borderwidth=0)]

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
        self.labels = self.display(0, [tk.Label(self, text=f"ID   {idi['contnombre'][k]}   {idi['conttel'][k]}"
                                                           f"   {idi['contcel'][k]}   {idi['contcorreo'][k]}"
                                                           f"   {idi['contfoto'][k]}",
                                                font=("Roboto", 10), bg="#212121", fg="#0099CC")])
        self.mostrar(0, 0, self.labels)

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
        self.controlador = controlador
        self.actividades = WatchOs.Agenda()
        self.labels = self.display(0, [tk.Label(self,
                                                text=f"ID   {idi['agenfecha'][k]}   {idi['agenhora'][k]}   "
                                                     f"{idi['agenevento'][k]}"
                                                     f"\n----------------------------------"
                                                     f"-----------------------------------", font=("Roboto", 10))])
        self.mostrar(0, self.labels)

    def display(self, i, result):
        """
        :param i: int
        :param result: lista de labels
        :return: result
        Crea una lista de Labels necesarias para sostener todas las habilidades guardadas.
        """
        actv = self.actividades.agenda
        if i < len(actv):
            result += [tk.Label(self, text=f"{actv[i].identidad}   {actv[i].fecha}   {actv[i].hora}   "
                                           f"{actv[i].info}", font=("Roboto", 10))]
            return self.display(i + 1, result)
        else:
            return result

    def mostrar(self, i, labels):
        if i < len(labels):
            labels[i].grid(row=i, column=0, padx=5, sticky="w")

            self.mostrar(i + 1, labels)


class CalculadoraUI(tk.Frame):
    def __init__(self, master, controlador):
        tk.Frame.__init__(self, master)
        self.temp = tk.Label(self, text="WIP")
        self.temp.pack()


if __name__ == "__main__":
    Comienzo()
