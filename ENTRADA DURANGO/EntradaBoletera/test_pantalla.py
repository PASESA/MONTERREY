from datetime import datetime, timedelta
from escpos.printer import Usb
import traceback
import tkinter as tk
from operacion import Operacion
from time import sleep
from enum import Enum


class Colors(Enum):
    """
    Enumeración que representa colores predefinidos.

    Cada color tiene un nombre asociado y un código hexadecimal.
    """
    # Códigos hexadecimales para los colores
    GREEN:str = "#00FF00"
    RED:str = "#FF0000"

class Alerts(Enum):
    """
    Enumeración de mensajes con descripciones.

    Los miembros de esta enumeración representan mensajes comunes
    y tienen asociadas cadenas descriptivas.
    """
    AUTO_EXISTS:str = "Hay auto"
    AUTO_NOT_EXISTS:str = "No hay auto"

    BUTTON_PRESSED:str = "Boton presionado."
    BUTTON_NOT_PRESSED:str = "Boton sin precionar"

class System_Messages(Enum):
    """
    Enumeración de mensajes con descripciones.

    Los miembros de esta enumeración representan mensajes comunes
    y tienen asociadas cadenas descriptivas.
    """
    TAKE_TICKET:str = "Tome su boleto\n"
    NOT_AUTO:str = "No hay auto\n"

    NOT_EXIST_PENSION:str = "No existe Pensionado\n"
    DESACTIVATE_CARD:str = "Tarjeta desactivada\n"

    PENSION_INSIDE:str = "El Pensionado ya está dentro\n"
    PENSION_EXPIRED:str = "Pensión vencida\n"

    PROCEED:str = "Avance\n"
    PRESS_BUTTON:str = "Precione boton\n"
    ERROR:str = "Ha ocurrido un error\n Lea nuevamente la tarjeta"

    NONE_MESAGE:str = "...\n"

class Pines(Enum):
    PIN_BARRERA:int = 17
    PIN_BOTON:int = 20
    PIN_SENSOR_AUTO:int = 21
    PIN_SENSOR_BOLETO:int = 16


    PIN_INDICADOR_BARRERA:int = 27
    PIN_INDICADOR_BOTON:int = 18

    PIN_INDICADOR_SENSOR_AUTO:int = 22
    PIN_INDICADOR_SENSOR_BOLETO:int = 0

class State(Enum):
    ON = 0
    OFF = 1

import RPi.GPIO as io           # Importa libreria de I/O (entradas / salidas)

Pines.PIN_SENSOR_AUTO.value = 21                      #gpio5,pin29,entrada loop                    
Pines.PIN_BOTON.value = 20                     #gpio6,pin31,entrada boton
Pines.PIN_SENSOR_BOLETO.value = 16                #gpio13,pin33,sensor boleto
Pines.PIN_BARRERA.value = 17                  #gpio17,pin11,Salida barrera

Pines.PIN_INDICADOR_SENSOR_AUTO.value = 22                     #gpio22,pin15,Salida indicador loop
Pines.PIN_INDICADOR_BOTON.value = 18                     #gpio18,pin12,Salida indicador boton
Pines.PIN_INDICADOR_BARRERA.value = 27                     #gpio27,pin13,Salida indicador barrera

io.setmode(io.BCM)              # modo in/out pin del micro
io.setwarnings(False)           # no señala advertencias de pin ya usados

io.setup(Pines.PIN_SENSOR_AUTO.value,io.IN)             # configura en el micro las entradas
io.setup(Pines.PIN_BOTON.value,io.IN)             # configura en el micro las entradas
io.setup(Pines.PIN_SENSOR_BOLETO.value,io.IN)             # configura en el micro las entradas


io.setup(Pines.PIN_BARRERA.value,io.OUT)           # configura en el micro las salidas
io.setup(Pines.PIN_INDICADOR_SENSOR_AUTO.value,io.OUT)           # configura en el micro las salidas
io.setup(Pines.PIN_INDICADOR_BOTON.value,io.OUT)
io.setup(Pines.PIN_INDICADOR_BARRERA.value,io.OUT)  

io.output(Pines.PIN_BARRERA.value,1)
io.output(Pines.PIN_INDICADOR_SENSOR_AUTO.value,1)
io.output(Pines.PIN_INDICADOR_BOTON.value,1)
io.output(Pines.PIN_INDICADOR_BARRERA.value,1)

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

fullscreen = False



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
            self.root.bind("<F11>", self.enter_fullscreen)
            self.root.bind("<Escape>", self.exit_fullscreen)

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

    def SenBoleto(self): #Detecta presencia de boleto
        global BanSenBoleto
        if io.input(Pines.PIN_SENSOR_BOLETO.value):
            io.output(Pines.PIN_INDICADOR_BARRERA.value ,State.OFF.value)#con un "1" se apaga el led
            BanSenBoleto = State.OFF.value
            print('no siente boleto')

        else:                
            io.output(Pines.PIN_INDICADOR_BARRERA.value ,State.ON.value)                              
            BanSenBoleto = State.ON.value
            print('siente boleto')

    def Intloop(self): #Detecta presencia de automovil
        global BanLoop
        if io.input(Pines.PIN_SENSOR_AUTO.value):
            print('no hay auto') 
            io.output(Pines.PIN_INDICADOR_SENSOR_AUTO.value ,State.OFF.value)#con un "1" se apaga el led              
            BanLoop = State.OFF.value

        else:
            print('hay auto') 
            io.output(Pines.PIN_INDICADOR_SENSOR_AUTO.value ,State.ON.value)
            BanLoop = State.ON.value

    def IntBoton(self): #Detecta presion de boton
        global BanBoton
        if io.input(Pines.PIN_BOTON.value):
            print('solto boton')
            io.output(Pines.PIN_INDICADOR_BOTON.value ,State.OFF.value)
            BanBoton = State.OFF.value

        else:
            print('presiono boton')            
            io.output(Pines.PIN_INDICADOR_BOTON.value ,State.ON.value)
            BanBoton = State.ON.value

    io.add_event_detect(Pines.PIN_SENSOR_AUTO.value, io.BOTH, callback = Intloop)
    io.add_event_detect(Pines.PIN_BOTON.value, io.BOTH, callback = IntBoton)
    io.add_event_detect(Pines.PIN_SENSOR_BOLETO.value, io.BOTH, callback = SenBoleto)

    def check_inputs(self):
        global BanBoton
        global BanLoop
        global BanImpresion
    
        if BanLoop == State.ON.value:
            self.change_info_label(self.label_auto, Alerts.AUTO_EXISTS, Colors.GREEN)
            tarjeta = self.entry_numero_tarjeta.get()
            if len(tarjeta) == 10:
                self.Pensionados(self)
        else:
            self.change_info_label(self.label_auto, Alerts.AUTO_NOT_EXISTS, Colors.RED)
            print("No ejecuta Pensionado")
            self.variable_numero_tarjeta.set("")               
            self.entry_numero_tarjeta.focus()
            BanImpresion = State.ON.value

        if BanBoton == State.ON.value:
            self.change_info_label(self.label_boton, Alerts.BUTTON_PRESSED, Colors.GREEN)
            print("BanSenBoleto ",str(BanSenBoleto))
            print("BanImpresion ",str(BanImpresion))
            print("BamLoop ",str(BanLoop))

            if BanLoop ==State.ON.value and BanImpresion == State.ON.value:
                print('imprimir boleto')
                self.agregarRegistroRFID()

                self.abrir_barrera()

                #BanImpresion = 0
                BanImpresion = State.OFF.value
                if BanSenBoleto == State.OFF.value:
                    print("En BanSenBoleto= 1 "+str(BanSenBoleto))

                else:
                    self.show_message(System_Messages.TAKE_TICKET)

            else:
                self.show_message(System_Messages.PRESS_BUTTON)
                print ('no puede imprimir porque no tiene Auto')

        else:
            self.change_info_label(self.label_boton, Alerts.BUTTON_NOT_PRESSED, Colors.RED)

            # if BanImpresion == 1: #and BanSenBoleto == 1:# mando a imprimir y ya no tiene boleto en la boquilla
            #     self.SenBol.config(text = "No siente boleto ")



        # Con un "1" se apaga el led
        io.output(Pines.PIN_INDICADOR_BARRERA.value, State.OFF.value)


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
        io.output(Pines.PIN_INDICADOR_BARRERA.value,State.OFF.value)

        # Con un "0" abre la barrera
        io.output(Pines.PIN_BARRERA.value, State.ON.value)
        sleep(1)
        io.output(Pines.PIN_BARRERA.value, State.OFF.value)

        print('------------------------------')
        print("****** Se abre barrera *******")
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
        self.entry_numero_tarjeta.focus()

    def change_info_label(self, label:tk.Label, new_text:Alerts, new_color:Colors) -> None:
        """
        Cambia el mensje de la etiqueta espeficicada asi como su color.

        :param label (tk.Label): Etiqueta a modificar.
        :param new_text (System_Messages): Mensaje a mostrar.
        :param new_color (Colors): Nuevo color para la etiqueta.

        :return: None
        """
        label.config(text=new_text.value, background=new_color.value)

    def enter_fullscreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)
        self.entry_numero_tarjeta.focus() 

    def exit_fullscreen(self, event):
        self.entry_numero_tarjeta.focus()
        self.fullScreenState = False
        self.root.attributes("-fullscreen", self.fullScreenState)




if __name__ == '__main__':
    Entrada()

