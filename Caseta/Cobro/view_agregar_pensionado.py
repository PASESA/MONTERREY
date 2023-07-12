from tkinter import messagebox as mb
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar, IntVar

from datetime import datetime

from queries import pensionados


class View_agregar_pensionados:

	def __init__(self):
		self.query = pensionados()

		# Crea la ventana principal
		self.panel_crud = tk.Toplevel()

		# Se elimina la funcionalidad del botón de cerrar
		self.panel_crud.protocol("WM_DELETE_WINDOW", lambda: self.desconectar())

		# Deshabilita los botones de minimizar y maximizar
		# self.panel_crud.attributes('-toolwindow', True)

		self.panel_crud.title(f'Agregar pensionado')

		# Configura la columna principal del panel para que use todo el espacio disponible
		self.panel_crud.columnconfigure(0, weight=1)

		self.variable_numero_tarjeta = StringVar()

		self.variable_nombre = StringVar()

		self.variable_apellido_1 = StringVar()
		self.variable_apellido_2 = StringVar()
		self.variable_fecha_alta = StringVar()
		self.telefono_1 = StringVar()
		self.telefono_2 = StringVar()

		self.ciudad = StringVar()
		self.colonia = StringVar()
		self.cp = StringVar()
		self.numero_calle = StringVar()

		self.placas = StringVar()
		self.auto_modelo = StringVar()
		self.auto_color = StringVar()

		self.vigencia = StringVar()
		self.fecha_vigencia = StringVar()
		self.monto = IntVar()
		self.estatus = StringVar()
		self.cortesia = StringVar()
		self.tolerancia = IntVar()



		self.registros = None

		# Llama a la función interface() que configura la interfaz gráfica
		self.interface()


		# # Calcula la posición de la ventana en la pantalla
		# pos_x = int(self.seccion_tabla.winfo_screenwidth() / 2)
		# pos_y = int(self.seccion_tabla.winfo_screenheight() / 2)

		# # Establece la geometría de la ventana con su posición y tamaño
		# self.panel_crud.geometry(f"+{pos_x}+{pos_y}")
		self.panel_crud.resizable(False, False)

		# Inicia el loop principal de la ventana
		self.panel_crud.mainloop()

	def interface(self):
		"""
		Crea toda la interface para cambiar de conexion

		:param None: 

		:raises None: 

		:return:
			- None
		"""
		# Se crea un Label Frame principal para la sección superior
		seccion_superior = ttk.LabelFrame(self.panel_crud, text='')
		seccion_superior.columnconfigure(1, weight=1)
		seccion_superior.propagate(True)
		seccion_superior.grid(row=0, column=0, sticky=tk.NSEW)

		##########################################################################################################

		# Se crea un Label Frame para la sección de la conexión
		etiqueta_user = ttk.Label(seccion_superior, text=f'Bienvenido/a')
		etiqueta_user.grid(row=0, column=1, padx=5, pady=5)


		seccion_datos_pensionado = ttk.LabelFrame(self.panel_crud, text="\tIngresa los datos del pensionado a registrar")
		seccion_datos_pensionado.grid(row=1, column=0,padx=10, pady=10)



		self.lbldatos0=ttk.Label(seccion_datos_pensionado, text="Num. Tarjeta:")
		self.lbldatos0.grid(column=0, row=1, padx=4, pady=4)   
    
		self.lbldatos1=ttk.Label(seccion_datos_pensionado, text="Nombre Empresa:")
		self.lbldatos1.grid(column=0, row=2, padx=4, pady=4)
		self.lbldatos2=ttk.Label(seccion_datos_pensionado, text="Nombre Contacto:")
		self.lbldatos2.grid(column=0, row=3, padx=4, pady=4)
		self.lbldatos3=ttk.Label(seccion_datos_pensionado, text="Apellido Contacto:")
		self.lbldatos3.grid(column=0, row=4, padx=4, pady=4)
		self.lbldatos4=ttk.Label(seccion_datos_pensionado, text="Telefono:")
		self.lbldatos4.grid(column=0, row=5, padx=4, pady=4)
		self.lbldatos5=ttk.Label(seccion_datos_pensionado, text="Telefono Opcional:")
		self.lbldatos5.grid(column=0, row=6, padx=4, pady=4)

		
		######Direccion del Pensionado
		self.lbldatos6=ttk.Label(seccion_datos_pensionado, text="--Direccion del Pensionado--")
		self.lbldatos6.grid(column=2, row=0, padx=8, pady=8)
		self.lbldatos7=ttk.Label(seccion_datos_pensionado, text="Calle y Numero:")
		self.lbldatos7.grid(column=2, row=1, padx=4, pady=4) 
		self.lbldatos8=ttk.Label(seccion_datos_pensionado, text="Colonia:")
		self.lbldatos8.grid(column=2, row=2, padx=4, pady=4)
		self.lbldatos9=ttk.Label(seccion_datos_pensionado, text="Ciudad/Estado:")
		self.lbldatos9.grid(column=2, row=3, padx=4, pady=4) 
		self.lbldatos10=ttk.Label(seccion_datos_pensionado, text="C.P.:")
		self.lbldatos10.grid(column=2, row=4, padx=4, pady=4) 

		
		######Datos del Auto
		self.lbldatos11=ttk.Label(seccion_datos_pensionado, text="--Datos del Auto--")
		self.lbldatos11.grid(column=0, row=8, padx=8, pady=8)
		self.lbldatos12=ttk.Label(seccion_datos_pensionado, text="Placas:")
		self.lbldatos12.grid(column=0, row=9, padx=4, pady=4) 
		self.lbldatos13=ttk.Label(seccion_datos_pensionado, text="Modelo:")
		self.lbldatos13.grid(column=0, row=10, padx=4, pady=4)
		self.lbldatos14=ttk.Label(seccion_datos_pensionado, text="Color:")
		self.lbldatos14.grid(column=0, row=11, padx=4, pady=4)

		#####Datos del Cobro
		self.lbldatos11=ttk.Label(seccion_datos_pensionado, text="--Datos del Cobro--")
		self.lbldatos11.grid(column=2, row=8, padx=8, pady=8)
		self.lbldatos12=ttk.Label(seccion_datos_pensionado, text="Monto x Mes:")
		self.lbldatos12.grid(column=2, row=9, padx=4, pady=4) 
		self.lbldatos13=ttk.Label(seccion_datos_pensionado, text="Cortesia:")
		self.lbldatos13.grid(column=2, row=10, padx=4, pady=4)
		self.lbldatos14=ttk.Label(seccion_datos_pensionado, text="Tolerancia:")
		self.lbldatos14.grid(column=2, row=11, padx=4, pady=4)
		

		self.entryMontoxmes=ttk.Entry(seccion_datos_pensionado, width=15, textvariable=self.Montoxmes)
		self.entryMontoxmes.grid(column=3, row=9)
		self.comboCortesia = ttk.Combobox(seccion_datos_pensionado, width=5, justify=tk.LEFT, state="readonly")
		self.comboCortesia["values"] = ["Si", "No"]
		self.comboCortesia.current(1)
		self.comboCortesia.grid(column=3, row=10, padx=1, pady=1)

		self.entryTole=ttk.Entry(seccion_datos_pensionado, width=15, textvariable=self.Tole)
		self.entryTole.grid(column=3, row=11)





		# Crea un botón y lo empaqueta en la seccion_botones_consulta
		boton_agregar_pensionado = ttk.Button(self.panel_crud,  text='Agregar usuario', command = self.agregar_pensionado, width=16)
		boton_agregar_pensionado.grid(row=2, column=0, padx=5, pady=5)

		self.campo_nombre_usuario.focus()

	def agregar_pensionado(self):
		try:
			usuario_nombre = self.usuario_nombre.get()
			usuario_contraseña = self.usuario_contraseña.get()
			usuario_nombre_completo = self.usuario_nombre_completo.get()
			usuario_fecha_alta =  datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			usuario_telefono = self.usuario_telefono.get()
			usuario_telefono_emergencia = self.usuario_telefono_emergencia.get()
			usuario_sucursal = self.usuario_sucursal.get()

			if len(usuario_nombre) == 0 or len(usuario_contraseña) == 0 or len(usuario_nombre_completo) == 0 or len(usuario_fecha_alta) == 0 or len(usuario_telefono) == 0 or len(usuario_telefono_emergencia) == 0 or len(usuario_sucursal) == 0:raise IndexError("No dejar campos en blanco")

			datos_usuario = [usuario_nombre, usuario_contraseña,  usuario_nombre_completo, usuario_fecha_alta,  usuario_telefono,  usuario_telefono_emergencia,  usuario_sucursal]

			self.query.agregar_pensionados(datos_usuario)

			self.desconectar()
		except Exception as e:
			mb.showerror("Error", e)
		except IndexError as e:
			mb.showerror("Error", e)






	def desconectar(self):
		"""
		Cierra la ventana principal y detiene el hilo en el que se ejecuta.

		:param None: 

		:raises None: 

		:return:
			- None
		"""
		#detener el loop principal
		self.panel_crud.quit()
		# Destruye el panel principal
		self.panel_crud.destroy()

