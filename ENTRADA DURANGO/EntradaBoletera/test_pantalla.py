from datetime import datetime, timedelta
from escpos.printer import Usb
import traceback
import tkinter as tk
from tkinter import ttk

import operacion
import time
# import RPi.GPIO as io           # Importa libreria de I/O (entradas / salidas)

# loop = 21                      #gpio5,pin29,entrada loop                    
# boton = 20                     #gpio6,pin31,entrada boton
# SenBBoleto = 16                #gpio13,pin33,sensor boleto
# barrera = 17                  #gpio17,pin11,Salida barrera
# out1 = 22                     #gpio22,pin15,Salida indicador loop
# out2 = 18                     #gpio18,pin12,Salida indicador boton
# out3 = 27                     #gpio27,pin13,Salida indicador barrera

# io.setmode(io.BCM)              # modo in/out pin del micro
# io.setwarnings(False)           # no señala advertencias de pin ya usados
# io.setup(loop,io.IN)             # configura en el micro las entradas
# io.setup(boton,io.IN)             # configura en el micro las entradas
# io.setup(SenBBoleto,io.IN)             # configura en el micro las entradas
# io.setup(barrera,io.OUT)           # configura en el micro las salidas
# io.setup(out1,io.OUT)           # configura en el micro las salidas
# io.setup(out2,io.OUT)
# io.setup(out3,io.OUT)  

# io.output(barrera,1)
# io.output(out1,1)
# io.output(out2,1)
# io.output(out3,1)

# BanLoop =1
# BanBoton=1
# BanSenBoleto=0
# BanImpresion=0 #No ha impreso

logo_1 = "LOGO1.jpg"
AutoA = "AutoA.png"
qr_imagen = "reducida.png"


font_entrada = ('Arial', 20)
font_entrada_negritas = ('Arial', 20, 'bold')
font_mensaje = ('Arial', 40)
font_reloj = ('Arial', 65)

font_etiquetas = ('Arial', 30, 'bold')


button_color = "#062546"#"#39acec""#6264d4"
button_letters_color = "white"


class Entrada:
    def __init__(self):
        self.folio_auxiliar = None

        self.DB=Operacion()
        self.root=tk.Tk()
        self.root.title(f"{nombre_estacionamiento} Entrada")

        # Obtener el ancho y alto de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Configura la ventana para que ocupe toda la pantalla
        # self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Colocar el LabelFrame en las coordenadas calculadas
        self.principal = tk.LabelFrame(self.root)
        self.principal.pack(expand=True, padx=5, pady=5, anchor='n')

        self.ExpedirRfid()
        self.check_inputs()

        self.root.mainloop()
        ###########################Inicia Pagina1##########################

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








        frame_boton=tk.Frame(frame_datos_entrada)
        frame_boton.grid(column=2, row=0, padx=2, pady=2)



       

        frame_info = tk.LabelFrame(seccion_entrada)#, background = '#CCC')
        frame_info.grid(column=0, row=2, padx=2, pady=2)

        self.label_informacion = tk.Label(frame_info, text="PRECIONE BOTON", width=25, font=font_mensaje, justify='center')
        self.label_informacion.grid(column=0, row=0, padx=2, pady=2)



        frame_inferior = tk.LabelFrame(seccion_entrada)
        frame_inferior.grid(column=0, row=3, padx=2, pady=2)


        frame_info_placa=tk.Frame(frame_inferior)
        frame_info_placa.grid(column=0, row=0, padx=2, pady=2)

        self.Placa=tk.StringVar()
        self.entry_placa=tk.Entry(frame_info_placa, width=50, textvariable=self.Placa, font=('Arial', 10, 'bold'), justify='center')
        self.entry_placa.bind('<Return>', self.Pensionados)
        self.entry_placa.grid(column=0, row=0, padx=2, pady=2)



        frame_reloj = tk.Frame(frame_inferior)
        frame_reloj.grid(column=0, row=1, padx=2, pady=2)

        self.Reloj = tk.Label(frame_reloj, text="Reloj", background="white", font=font_reloj, justify='center')
        self.Reloj.grid(column=0, row=0, padx=2, pady=2)



        frame_etiquetas = tk.Frame(frame_inferior)
        frame_etiquetas.grid(column=0, row=2, padx=2, pady=2)

        label_auto = tk.Label(frame_etiquetas, text="No hay auto", width=15, font=font_etiquetas, justify='center', background="#00FF00")
        label_auto.grid(column=0, row=0, padx=2, pady=2)

        label_boton = tk.Label(frame_etiquetas, text=" Boton sin precionar ", width=15, font=font_etiquetas, justify='center', background="#FF0000")
        label_boton.grid(column=1, row=0, padx=2, pady=2)





        self.entry_placa.focus()


    def SenBoleto(self): #Detecta presencia de automovil
        global SenBBoleto
        # if io.input(SenBBoleto):
                 
        #         io.output(out3,1)#con un "1" se apaga el led
        #         #self.loopDet.config(text = "Inicio", background = '#CCC')                
        #         BanSenBoleto = 1
        #         print('no siente boleto '+str(BanSenBoleto))
        #         #self.check_inputs()
        # else:                
                 
        #         io.output(out3,0)                              
        #         #self.loopDet.config(text = "Auto", background = 'red')
        #         BanSenBoleto = 0
        #         print('siente boleto '+str(BanSenBoleto))
        #         #self.check_inputs()


    def Intloop(self): #Detecta presencia de automovil
        global BanLoop
        # if io.input(loop):
        #         print('no hay auto') 
        #         io.output(out1,1)#con un "1" se apaga el led
        #         #self.loopDet.config(text = "Inicio", background = '#CCC')                
        #         BanLoop = 1
        #         #BanImpresion = 0
        #         #self.check_inputs()
        # else:                
        #         print('hay auto') 
        #         io.output(out1,0)                              
        #         #self.loopDet.config(text = "Auto", background = 'red')
        #         BanLoop = 0
        #         #self.check_inputs()


    def IntBoton(self): #Detecta presencia de automovil
        global BanBoton
    #     if io.input(boton):
    #                     #self.BotDet.config(text = "Presione Boton",background="#CCC")
    #                     print('solto boton')
    #                     io.output(out2,1)
    #                     BanBoton = 1
    #     else:
    #                     print('presiono boton')            
    #                     io.output(out2,0)
    #                     #self.BotDet.config(text = "Imprimiendo",background="red")
    #                     BanBoton = 0
    #                     #self.agregarRegistroRFID()

    # io.add_event_detect(loop, io.BOTH, callback = Intloop)
    # io.add_event_detect(boton, io.BOTH, callback = IntBoton)
    # io.add_event_detect(SenBBoleto, io.BOTH, callback = SenBoleto)



    def check_inputs(self):
        global BanBoton
        global BanLoop
        global BanImpresion
    
        # if BanLoop == 0:
        #         self.loopDet.config(text = " hay auto", background = 'green')
        #         tarjeta=str(self.entryNumTarjeta4.get(),)
        #         if len(tarjeta) == 10:
        #             #mb.showwarning("IMPORTANTE", "ENTRO")
        #             self.Pensionados(self)
        # else:
        #         self.loopDet.config(text = "No Siente Auto", background = '#CCC')
        #         self.labelMensaje.config(text= "No ejecuta Pensionado")
        #         self.NumTarjeta4.set("")               
        #         self.entryNumTarjeta4.focus()
        #         BanImpresion = 0
        # if (BanBoton == 1):#BanBoton == 1 no esta oprimido el boton
        #     self.BotDet.config(text = "solto Boton ",background="#CCC")
        #     #print(str(BanSenBoleto))
        #     if BanImpresion == 1: #and BanSenBoleto == 1:# mando a imprimir y ya no tiene boleto en la boquilla
        #         self.SenBol.config(text = "No siente boleto ")
        #         #print("En BanBoton= 1 "+str(BanSenBoleto))

        #                             #io.output(out2,1)
        # else:    
        #         self.BotDet.config(text = "presiono Boton imprime ",background="green")
        #         # print("BanSenBoleto ",str(BanSenBoleto))
        #         # print("BanImpresion ",str(BanImpresion))
        #         # print("BamLoop ",str(BanLoop))
        #         # if BanLoop==0 and BanImpresion == 0:
        #         #     #io.output(out2,0)             
        #         #    print('imprimir')
        #         #    #print(str(BanSenBoleto))
        #         #    self.agregarRegistroRFID()
        #         #    io.output(out3,1)#con un "1" se apaga el led
        #         #    io.output(barrera,0)#con un "0" abre la barrera
        #         #    time.sleep (1)
        #         #    io.output(barrera,1)
        #         #    #BanImpresion = 0
        #         #    BanImpresion = 1
        #         #    if BanSenBoleto == 1:
        #         #       print("En BanSenBoleto= 1 "+str(BanSenBoleto))
        #         #       # self.SenBol.config(text = "No siente boleto ")
        #         #       # io.output(out3,1)#con un "1" se apaga el led
        #         #        #io.output(barrera,0)#con un "0" abre la barrera
        #         #        #time.sleep (1)
        #         #        #io.output(barrera,1)
        #         #    else:                   
        #         #       self.SenBol.config(text = "siente boleto ")
                    
        #         # else:
        #         #    print ('no puede imprimir porque no tiene Auto')
        #         #    #print(str(BanSenBoleto))
        #         #    self.BotDet.config(text = "no puede imprimir no hay auto ",background="red")



        fecha_hora =datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        self.Reloj.config(text=fecha_hora)            
        self.root.after(60, self.check_inputs)


    def agregarRegistroRFID(self):
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
        printer.text('Monterrey No. 75\n')
        printer.text('Entrada Durango \n')
        printer.set(align = "left")
        printer.image(qr_imagen)

        printer.text("--------------------------------------\n")
        printer.cut()

        printer.close()

        self.DB.altaRegistroRFID(datos)
        self.Placa.set('')




    def Pensionados(self, event):
        try:
            numtarjeta=self.NumTarjeta4.get()

            print(numtarjeta)
            Existe = self.DB.ValidarPen(numtarjeta)
            tarjeta = int(Existe)

            if len(Existe) == 0:
                self.label_informacion.config(text="No existe Pensionado")
                self.NumTarjeta4.set("")
                self.entryNumTarjeta4.focus()
                return

            respuesta = self.DB.ConsultaPensionado(Existe)

            for fila in respuesta:
                VigAct = fila[0]
                Estatus = fila[1]
                Tolerancia = int(fila[3])

            if VigAct is None:
                self.label_informacion.config(text="Tarjeton desactivado")
                self.Placa.set("")
                self.entry_placa.focus()
                return

            elif Estatus == 'Adentro':
                self.label_informacion.config(text="El Pensionado ya está dentro")
                self.Placa.set("")
                self.entry_placa.focus()
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
                self.label_informacion.config(text="Vigencia Vencida")
                self.Placa.set("")
                self.entry_placa.focus()
                return

            datos = (Existe, tarjeta, hoy, 'Adentro', 0)
            datos1 = ('Adentro', Existe)
            self.DB.MovsPensionado(datos)
            self.DB.UpdPensionado(datos1)

            self.NumTarjeta4.set("")               
            self.entryNumTarjeta4.focus()

            self.abrir_barrera()

        except Exception as e:
            print(e)
            traceback.print_exc()
            self.label_informacion.config(text="Ha ocurrido un error")
            self.Placa.set("")
            self.entry_placa.focus()
            return


    def abrir_barrera(self):
        """Esta funcion se encarga de abrir la barrera."""
        # # Con un "1" se apaga el led
        # io.output(out3,1)

        # # Con un "0" abre la barrera
        # io.output(out1, 0)
        # sleep(1)
        # io.output(out1, 1)

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







instancia = Entrada()