from datetime import datetime, timedelta
from escpos.printer import Usb
import traceback
import tkinter as tk
from tkinter import ttk

from operacion import Operacion
from time import sleep
import RPi.GPIO as io           # Importa libreria de I/O (entradas / salidas)

loop = 21                      #gpio5,pin29,entrada loop                    
boton = 20                     #gpio6,pin31,entrada boton
SenBBoleto = 16                #gpio13,pin33,sensor boleto
barrera = 17                  #gpio17,pin11,Salida barrera
out1 = 22                     #gpio22,pin15,Salida indicador loop
out2 = 18                     #gpio18,pin12,Salida indicador boton
out3 = 27                     #gpio27,pin13,Salida indicador barrera

io.setmode(io.BCM)              # modo in/out pin del micro
io.setwarnings(False)           # no señala advertencias de pin ya usados
io.setup(loop,io.IN)             # configura en el micro las entradas
io.setup(boton,io.IN)             # configura en el micro las entradas
io.setup(SenBBoleto,io.IN)             # configura en el micro las entradas
io.setup(barrera,io.OUT)           # configura en el micro las salidas
io.setup(out1,io.OUT)           # configura en el micro las salidas
io.setup(out2,io.OUT)
io.setup(out3,io.OUT)  

io.output(barrera,1)
io.output(out1,1)
io.output(out2,1)
io.output(out3,1)

BanLoop =1
BanBoton=1
BanSenBoleto=0
BanImpresion=0 #No ha impreso

logo_1 = "LOGO1.jpg"
AutoA = "AutoA.png"
qr_imagen = "reducida.png"

nombre_estacionamiento = 'Monterrey 75'
nombre_entrada = "Durango"

font_entrada = ('Arial', 20)
font_entrada_negritas = ('Arial', 20, 'bold')
font_mensaje = ('Arial', 40)
font_reloj = ('Arial', 65)

font_etiquetas = ('Arial', 30, 'bold')

fullscreen = True

from enum import Enum
class Colors(Enum):
    """
    Enumeración que representa colores predefinidos.

    Cada color tiene un nombre asociado y un código hexadecimal.
    """
    # Códigos hexadecimales para los colores
    GREEN = "#00FF00"
    RED = "#FF0000"

class Alerts(Enum):
    """
    Enumeración de mensajes con descripciones.

    Los miembros de esta enumeración representan mensajes comunes
    y tienen asociadas cadenas descriptivas.
    """
    AUTO_EXISTS = "Hay auto"
    AUTO_NOT_EXISTS = "No hay auto"

    BUTTON_PRESSED = "Boton presionado."
    BUTTON_NOT_PRESSED = "Boton sin precionar"

class System_Messages(Enum):
    """
    Enumeración de mensajes con descripciones.

    Los miembros de esta enumeración representan mensajes comunes
    y tienen asociadas cadenas descriptivas.
    """
    NOT_EXIST_PENSION = "No existe Pensionado\n"
    DESACTIVATE_CARD = "Tarjeta desactivada\n"

    PENSION_INSIDE = "El Pensionado ya está dentro\n"
    PENSION_EXPIRED = "Pensión vencida\n"

    PROCEED = "Avance\n"
    PRESS_BUTTON = "Precione boton\n"
    ERROR = "Ha ocurrido un error\n Lea nuevamente la tarjeta"

    NONE_MESAGE = "...\n"

class Pines(Enum):
    PIN_SENSOR = 0
    PIN_BARRERA = 0
    PIN_BOTON = 0

class Entrada:
    def __init__(self):
        self.folio_auxiliar = None

        self.DB=Operacion()
        self.root=tk.Tk()
        self.root.title(f"{nombre_estacionamiento} Entrada {nombre_entrada}")

        if fullscreen:
            # Obtener el ancho y alto de la pantalla
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            # Configura la ventana para que ocupe toda la pantalla
            # self.root.geometry(f"{screen_width}x{screen_height}+0+0")

            self.root.attributes('-fullscreen', True)  
            self.fullScreenState = False
            self.root.bind("<F11>", self.toggleFullScreen)
            self.root.bind("<Escape>", self.quitFullScreen)

        # Colocar el LabelFrame en las coordenadas calculadas
        self.principal = tk.LabelFrame(self.root)
        self.principal.pack(expand=True, padx=5, pady=5, anchor='n')

        self.MaxId = tk.StringVar()
        self.variable_numero_tarjeta = tk.StringVar()
        self.Placa = tk.StringVar()

        self.ExpedirRfid()
        self.check_inputs()

        self.root.mainloop()


    def ExpedirRfid(self):
        seccion_entrada = tk.Frame(self.principal)
        seccion_entrada.grid(column=0, row=0, padx=2, pady=2, sticky=tk.NSEW)

        frame_bienvenida = tk.Frame(seccion_entrada)
        frame_bienvenida.grid(column=0, row=0, padx=2, pady=2)

        frame_mensaje_bienvenida = tk.Frame(frame_bienvenida)
        frame_mensaje_bienvenida.grid(column=0, row=0, padx=2, pady=2)

        # Asegura que la fila y la columna del frame se expandan con el contenedor
        frame_mensaje_bienvenida.grid_rowconfigure(0, weight=1)
        frame_mensaje_bienvenida.grid_columnconfigure(0, weight=1)

        label_entrada = tk.Label(frame_mensaje_bienvenida, text=f"Bienvenido(a)", font=font_mensaje, justify='center')
        label_entrada.grid(row=0, column=0)



        frame_datos_entrada = tk.Frame(seccion_entrada)
        frame_datos_entrada.grid(column=0, row=1, padx=2, pady=2)

        frame_info_cliente=tk.Frame(frame_datos_entrada)
        frame_info_cliente.grid(column=0, row=0, padx=2, pady=2)



        frame_info = tk.LabelFrame(seccion_entrada)#, background = '#CCC')
        frame_info.grid(column=0, row=2, padx=2, pady=2)

        self.label_informacion = tk.Label(frame_info, text=System_Messages.NONE_MESAGE.value, width=25, font=font_mensaje, justify='center')
        self.label_informacion.grid(column=0, row=0, padx=2, pady=2)



        frame_inferior = tk.LabelFrame(seccion_entrada)
        frame_inferior.grid(column=0, row=3, padx=2, pady=2)


        frame_info_placa=tk.Frame(frame_inferior)
        frame_info_placa.grid(column=0, row=0, padx=2, pady=2)

        self.entry_numero_tarjeta=tk.Entry(frame_info_placa, width=50, textvariable=self.variable_numero_tarjeta, font=('Arial', 10, 'bold'), justify='center')
        self.entry_numero_tarjeta.bind('<Return>', self.Pensionados)
        self.entry_numero_tarjeta.grid(column=0, row=0, padx=2, pady=2)

        frame_reloj = tk.Frame(frame_inferior)
        frame_reloj.grid(column=0, row=1, padx=2, pady=2)

        self.Reloj = tk.Label(frame_reloj, font=font_reloj, justify='center')
        self.Reloj.grid(column=0, row=0, padx=2, pady=2)



        frame_etiquetas = tk.Frame(frame_inferior)
        frame_etiquetas.grid(column=0, row=2, padx=2, pady=2)

        self.label_auto = tk.Label(frame_etiquetas, text=Alerts.AUTO_EXISTS.value, width=15, font=font_etiquetas, justify='center', background=Colors.GREEN.value)
        self.label_auto.grid(column=0, row=0, padx=2, pady=2)

        self.label_boton = tk.Label(frame_etiquetas, text=Alerts.BUTTON_PRESSED.value, width=15, font=font_etiquetas, justify='center', background=Colors.GREEN.value)
        self.label_boton.grid(column=1, row=0, padx=2, pady=2)





        self.entry_numero_tarjeta.focus()

    def SenBoleto(self): #Detecta presencia de automovil
        global SenBBoleto
        if io.input(SenBBoleto):
                 
                io.output(out3,1)#con un "1" se apaga el led
                #self.loopDet.config(text = "Inicio", background = '#CCC')                
                BanSenBoleto = 1
                print('no siente boleto '+str(BanSenBoleto))
                #self.check_inputs()
        else:                
                 
                io.output(out3,0)                              
                #self.loopDet.config(text = "Auto", background = 'red')
                BanSenBoleto = 0
                print('siente boleto '+str(BanSenBoleto))
                #self.check_inputs()

    def Intloop(self): #Detecta presencia de automovil
        global BanLoop
        if io.input(loop):
                print('no hay auto') 
                io.output(out1,1)#con un "1" se apaga el led
                #self.loopDet.config(text = "Inicio", background = '#CCC')                
                BanLoop = 1
                #BanImpresion = 0
                #self.check_inputs()
        else:                
                print('hay auto') 
                io.output(out1,0)                              
                #self.loopDet.config(text = "Auto", background = 'red')
                BanLoop = 0
                #self.check_inputs()

    def IntBoton(self): #Detecta presencia de automovil
        global BanBoton
        if io.input(boton):
                        #self.BotDet.config(text = "Presione Boton",background="#CCC")
                        print('solto boton')
                        io.output(out2,1)
                        BanBoton = 1
        else:
                        print('presiono boton')            
                        io.output(out2,0)
                        #self.BotDet.config(text = "Imprimiendo",background="red")
                        BanBoton = 0
                        #self.agregarRegistroRFID()

    io.add_event_detect(loop, io.BOTH, callback = Intloop)
    io.add_event_detect(boton, io.BOTH, callback = IntBoton)
    io.add_event_detect(SenBBoleto, io.BOTH, callback = SenBoleto)

    def check_inputs(self):
        global BanBoton
        global BanLoop
        global BanImpresion
    
        if BanLoop == 0:
                self.loopDet.config(text = " hay auto", background = 'green')
                tarjeta=str(self.entry_numero_tarjeta.get(),)
                if len(tarjeta) == 10:
                    self.Pensionados(self)
        else:
                self.loopDet.config(text = "No Siente Auto", background = '#CCC')
                self.labelMensaje.config(text= "No ejecuta Pensionado")
                self.variable_numero_tarjeta.set("")               
                self.entry_numero_tarjeta.focus()
                BanImpresion = 0
        if (BanBoton == 1):#BanBoton == 1 no esta oprimido el boton
            self.BotDet.config(text = "solto Boton ",background="#CCC")
            #print(str(BanSenBoleto))
            if BanImpresion == 1: #and BanSenBoleto == 1:# mando a imprimir y ya no tiene boleto en la boquilla
                self.SenBol.config(text = "No siente boleto ")
                #print("En BanBoton= 1 "+str(BanSenBoleto))

                                    #io.output(out2,1)
        else:    
                self.BotDet.config(text = "presiono Boton imprime ",background="green")
                print("BanSenBoleto ",str(BanSenBoleto))
                print("BanImpresion ",str(BanImpresion))
                print("BamLoop ",str(BanLoop))
                if BanLoop==0 and BanImpresion == 0:
                    #io.output(out2,0)             
                   print('imprimir')
                   #print(str(BanSenBoleto))
                   self.agregarRegistroRFID()

                   self.abrir_barrera()

                   #BanImpresion = 0
                   BanImpresion = 1
                   if BanSenBoleto == 1:
                      print("En BanSenBoleto= 1 "+str(BanSenBoleto))
                      # self.SenBol.config(text = "No siente boleto ")
                      # io.output(out3,1)#con un "1" se apaga el led
                       #io.output(barrera,0)#con un "0" abre la barrera
                       #time.sleep (1)
                       #io.output(barrera,1)
                   else:                   
                      self.SenBol.config(text = "siente boleto ")
                    
                else:
                   print ('no puede imprimir porque no tiene Auto')
                   #print(str(BanSenBoleto))
                   self.BotDet.config(text = "no puede imprimir no hay auto ",background="red")
        # Con un "1" se apaga el led
        io.output(out3,1)


        fecha_hora =datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        self.Reloj.config(text=fecha_hora)            
        self.root.after(60, self.check_inputs)

    def agregarRegistroRFID(self):
        """
        Agrega un registro RFID generando un boleto de entrada.

        :return: None
        """
        placa = self.Placa.get()
        Corte = 0

        MaxFolio=self.DB.MaxfolioEntrada()
        folio_boleto = MaxFolio + 1
        self.MaxId.set(folio_boleto)

        folio_cifrado = self.DB.cifrar_folio(folio = folio_boleto)
        # print(f"QR entrada: {folio_cifrado}")

        #Generar QR
        self.DB.generar_QR(folio_cifrado)

        fechaEntro = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        datos=(fechaEntro, Corte, placa)

        printer = Usb(0x04b8, 0x0e15, 0)

        # printer.image(logo_1)
        printer.text("--------------------------------------\n")
        printer.set("center")
        printer.text("BOLETO DE ENTRADA\n")
        printer.set(height=2, align='center')
        printer.text(f'Folio 000{folio_boleto}\n')

        printer.set("center")        
        printer.text(f'Entro: {fechaEntro[:-3]}\n')
        printer.text(f'{nombre_estacionamiento}\n')
        printer.text(f'Entrada {nombre_entrada}\n')
        printer.set(align = "left")
        printer.image(qr_imagen)

        printer.text("--------------------------------------\n")
        printer.cut()

        printer.close()

        self.DB.altaRegistroRFID(datos)

    def Pensionados(self, event):
        """
        Maneja la entrada de pensionados.

        :param event: Evento de teclado.
        :return: None
        """
        try:
            numtarjeta = self.variable_numero_tarjeta.get()
            # if numtarjeta ==  1:
            #     self.change_info_label(self.label_boton, Alerts.BUTTON_PRESSED, Colors.GREEN)
            #     self.change_info_label(self.label_auto, Alerts.AUTO_EXISTS, Colors.GREEN)

            # if numtarjeta ==  2:
            #     self.change_info_label(self.label_boton, Alerts.BUTTON_NOT_PRESSED, Colors.RED)
            #     self.change_info_label(self.label_auto, Alerts.AUTO_NOT_EXISTS, Colors.RED)

            # if numtarjeta ==  3:
            #     self.change_info_label(self.label_boton, Alerts.BUTTON_NOT_PRESSED, Colors.RED)
            #     self.change_info_label(self.label_auto, Alerts.AUTO_EXISTS, Colors.GREEN)

            # if numtarjeta ==  4:
            #     self.change_info_label(self.label_boton, Alerts.BUTTON_PRESSED, Colors.GREEN)
            #     self.change_info_label(self.label_auto, Alerts.AUTO_NOT_EXISTS, Colors.RED)


            # if numtarjeta ==  5:
            #     self.show_message(System_Messages.DESACTIVATE_CARD)

            # if numtarjeta ==  6:
            #     self.show_message(System_Messages.ERROR)

            # if numtarjeta ==  7:
            #     self.show_message(System_Messages.NOT_EXIST_PENSION)

            # if numtarjeta ==  8:
            #     self.show_message(System_Messages.PENSION_EXPIRED)

            # if numtarjeta ==  9:
            #     self.show_message(System_Messages.PENSION_INSIDE)

            # if numtarjeta ==  10:
            #     self.show_message(System_Messages.PRESS_BUTTON)

            # if numtarjeta ==  11:
            #     self.show_message(System_Messages.PROCEED)


            print(numtarjeta)
            Existe = self.DB.ValidarPen(numtarjeta)

            if len(Existe) == 0:
                self.show_message(System_Messages.NOT_EXIST_PENSION)
                return

            respuesta = self.DB.ConsultaPensionado(Existe)

            for fila in respuesta:
                VigAct = fila[0]
                Estatus = fila[1]
                Tolerancia = int(fila[3])

            if VigAct is None:
                self.show_message(System_Messages.DESACTIVATE_CARD)
                return

            elif Estatus == 'Adentro':
                self.show_message(System_Messages.PENSION_INSIDE)
                return

            # Obtener la fecha y hora actual en formato deseado
            VigAct = VigAct.strftime("%Y-%m-%d %H:%M:%S")
            # Convertir la cadena de caracteres en un objeto datetime
            VigAct = datetime.strptime(VigAct, "%Y-%m-%d %H:%M:%S")

            # Obtener la fecha y hora actual en formato deseado
            hoy = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            # Convertir la cadena de caracteres en un objeto datetime
            hoy = datetime.strptime(hoy, "%Y-%m-%d %H:%M:%S")

            limite = self.get_date_limit(VigAct, Tolerancia)
            print(limite)

            if hoy >= limite:
                self.show_message(System_Messages.PENSION_EXPIRED)
                return

            datos = (Existe, numtarjeta, hoy, 'Adentro', 0)
            datos1 = ('Adentro', Existe)
            self.DB.MovsPensionado(datos)
            self.DB.UpdPensionado(datos1)

            self.variable_numero_tarjeta.set("")               
            self.entry_numero_tarjeta.focus()

            self.abrir_barrera()

        except Exception as e:
            print(e)
            traceback.print_exc()
            self.show_message(System_Messages.ERROR)

    def abrir_barrera(self) -> None:
        """
        Abre la barrera.

        :return: None
        """
        self.show_message(System_Messages.PROCEED)
        sleep(1)
        # Con un "1" se apaga el led
        io.output(out3,1)

        # Con un "0" abre la barrera
        io.output(out1, 0)
        sleep(1)
        io.output(out1, 1)

        print('------------------------------')
        print("Se abre barrera")
        print('------------------------------')

    def get_date_limit(self, date_start:datetime, Tolerance:int) -> datetime:
        """
        Calcula la fecha límite a partir de una fecha de inicio y una cantidad de días de tolerancia.

        :param date_start (datetime): Fecha de inicio.
        :param Tolerance (int): Cantidad de días laborables a agregar.
        :return (datetime): Fecha límite después de agregar la cantidad de días laborables.
        """
        date_limit = date_start

        while Tolerance > 0:
            date_limit  += timedelta(days=1)
            # Verifica si el día no es fin de semana (lunes a viernes)
            if date_limit.weekday() < 5:
                Tolerance -= 1
        
        return date_limit

    def show_message(self, message: System_Messages) -> None:
        """
        Muestra un mensaje en la interfaz.

        :param message (str): Mensaje a mostrar.
        :return: None
        """
        self.label_informacion.config(text=message.value)
        self.variable_numero_tarjeta.set("")
        self.entry_numero_tarjeta

    def change_info_label(self, label:tk.Label, new_text:Alerts, new_color:Colors) -> None:
        """
        Cambia el mensje de la etiqueta espeficicada asi como su color.

        :param label (tk.Label): Etiqueta a modificar.
        :param new_text (System_Messages): Mensaje a mostrar.
        :param new_color (Colors): Nuevo color para la etiqueta.

        :return: None
        """
        label.config(text=new_text.value, background=new_color.value)

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)
        self.entry_numero_tarjeta.focus() 

    def quitFullScreen(self, event):
        self.entry_numero_tarjeta.focus()
        self.fullScreenState = False
        self.root.attributes("-fullscreen", self.fullScreenState)

instancia = Entrada()
