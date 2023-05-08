import pymysql
from tkinter import messagebox as mb
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import qrcode

class Operacion:

	def abrir(self):
		conexion=pymysql.connect(host="localhost",
								 user="root",
								 passwd="",
								 database="db_tenayuca")

		#conexion = pymysql.connect(host="192.168.1.91",
		#                   user="Aurelio",
		#                   passwd="RG980320",
		#                   database="Parqueadero1")
		return conexion


	def altaRegistroRFID(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="insert into Entradas(Entrada, CorteInc, Placas) values (%s,%s,%s)"
		cursor.execute(sql, datos)
		cone.commit()
		cone.close()

	def guardacobro(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update Entradas set vobo = %s, Importe = %s, TiempoTotal = %s, Entrada = %s, Salida = %s,TarifaPreferente = %s, QRPromo = %s where id = %s;"
		#sql = "update Entradas set vobo = %s, Importe = %s, TiempoTotal = %s, Entrada = %s, Salida = %s,TarifaPreferente = %s where id = %s;"
		cursor.execute(sql, datos)
		cone.commit()
		cone.close()

	#Se agrega Función para validar que la promoción no se aplique doble 15ago22
	def ValidaPromo(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select id from Entradas where QRPromo = %s "
		#sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql, datos)
		cone.close()
		return cursor.fetchall()  

	def consulta(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select Entrada, Salida from Entradas where id=%s"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql, datos)
		cone.close()
		return cursor.fetchall()

	def recuperar_todos(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select id, Entrada, Salida from Entradas"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def recuperar_sincobro(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select id, Entrada, Salida, Importe from Entradas where CorteInc = 0 and Importe is not null "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def desglose_cobrados(self,Numcorte):
		cone=self.abrir()
		cursor=cone.cursor()
		#sql="SELECT TarifaPreferente,Importe, Count(*) as cuantos FROM Entradas where CorteInc = 6 "
		#sql="SELECT TarifaPreferente,Importe, Count(*) as cuantos FROM Entradas where CorteInc = %s GROUP BY TarifaPreferente,Importe;"
		sql="SELECT Count(*),TarifaPreferente,Importe, Count(*)*Importe  as cuantos FROM Entradas where CorteInc = %s GROUP BY TarifaPreferente,Importe;"
		#sql="select id, Entrada, Salida, Importe from Entradas where CorteInc = 0 and Importe is not null "
		cursor.execute(sql,Numcorte)
		cone.close()
		return cursor.fetchall()
	def Autos_dentro(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select id, Entrada, Placas from Entradas where CorteInc = 0 and Importe is null and Salida is null "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def CuantosAutosdentro(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select count(*) from Entradas where CorteInc = 0 and Importe is null and Salida is null "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def Quedados_Sensor(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select Quedados from Cortes where Folio=%s"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql, datos)
		cone.close()
		return cursor.fetchall()

	def NumBolQued(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select NumBolQued from Cortes where Folio=%s"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql, datos)
		cone.close()
		return cursor.fetchall()
	def EntradasSensor(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select EntSens from AccesosSens where Folio=1"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def SalidasSensor(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select SalSens from AccesosSens where Folio=1"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def CuantosBoletosCobro(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select count(*) from Entradas where CorteInc = 0 and Importe is not null and Salida is not null "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def BEDCorte(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select count(*) from Entradas where ((vobo is null and TarifaPreferente is null) or (vobo = 'lmf' and TarifaPreferente = ''))"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def BAnteriores(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select count(*) from Entradas where vobo = 'ant' "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def corte(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select COALESCE(sum(importe), 0) from Entradas where CorteInc = 0"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def MaxfolioEntrada(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select max(id) from Entradas;"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def Maxfolio_Cortes(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select max(Folio) from Cortes;"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def ActualizarEntradasConcorte(self, maxnum):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update Entradas set CorteInc = %s, vobo = %s where TiempoTotal is not null and CorteInc=0;"
		#sql = "update Entradas set CorteInc=%s where TiempoTotal is not null and CorteInc=0;"
		cursor.execute(sql,maxnum)
		cone.commit()
		cone.close()

	def NocobradosAnt(self, vobo):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update Entradas set vobo = %s where Importe is null and CorteInc=0;"
		cursor.execute(sql,vobo)
		cone.commit()
		cone.close()

	def obtenerNumCorte(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select max(Folio) from Cortes"
		#sql = "update Entradas set CorteInc = 1 WHERE Importe > 0"
		cursor.execute(sql)
		#cone.commit()
		cone.close()
		return cursor.fetchall()
	def MaxnumId(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select max(idInicial) from Cortes"
		#sql = "update Entradas set CorteInc = 1 WHERE Importe > 0"
		cursor.execute(sql)
		#cone.commit()
		cone.close()
		return cursor.fetchall()

	def GuarCorte(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="insert into Cortes(Importe, FechaIni, FechaFin,Quedados,idInicial,NumBolQued) values (%s,%s,%s,%s,%s,%s)"
		#sql = "update Entradas set CorteInc = 1 WHERE Importe > 0"
		cursor.execute(sql,datos)
		cone.commit()
		cone.close()
	def UltimoCorte(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select min(inicio) from MovsUsuarios where CierreCorte is null;"
		#sql="select max(FechaFin) from Cortes;"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
		
 ######REPORTE EXCEL
	def Cortes_Max(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT max(Salida), max(Corteinc) FROM Entradas where MONTH(Salida)=%s AND YEAR(Salida)=%s "
		#sql="SELECT max(FechaFin), min(FechaFin) FROM Cortes where MONTH(FechaFin)=%s AND YEAR(FechaFin)=%s " 
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()
	def Cortes_Min(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT max(FechaIni), min(FechaIni) FROM Cortes where MONTH(FechaIni)=%s AND YEAR(FechaIni)=%s " 
		#sql="SELECT min(Entrada),min(Corteinc) FROM Entradas where MONTH(Entrada)=%s AND YEAR(Entrada)=%s AND CorteInc > 0 "
		#sql="SELECT max(FechaFin), min(FechaFin) FROM Cortes where MONTH(FechaFin)=%s AND YEAR(FechaFin)=%s " 
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()
	def Cortes_Folio(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT Folio FROM Cortes where FechaIni=%s"
		#sql="SELECT FechaIni, FechaFin FROM Cortes where Folio=%s" 
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()
	def Registros_corte(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT id, Entrada, Salida, TiempoTotal, Importe, CorteInc, Placas, TarifaPreferente FROM Entradas where CorteInc > (%s-1) AND CorteInc < (%s+1)"  #Entradas where Entrada >= %s AND Salida <= %s
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()
	def Totales_corte(self, datos1):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT sum(Importe), max(CorteInc), min(CorteInc), Count(TarifaPreferente) FROM Entradas where CorteInc > (%s-1) AND CorteInc < (%s+1)" #Entrada > %s AND Entrada < %s
		cursor.execute(sql,datos1)
		cone.close()
		return cursor.fetchall()
	def Resumen_promo(self, datos1):
		cone=self.abrir()
		cursor=cone.cursor()
		#print('Adentro del query')
		sql="SELECT Count(TarifaPreferente),TarifaPreferente,Importe, sum(Importe) as ImporteTot FROM Entradas where CorteInc > (%s-1) AND CorteInc < (%s+1) GROUP BY TarifaPreferente ORDER BY ImporteTot DESC;"
		#sql="SELECT Count(*),TarifaPreferente,Importe, Count(*)*Importe  as cuantos FROM Entradas where CorteInc = %s GROUP BY TarifaPreferente,Importe;"
		#print(Count(TarifaPreferente)+'  '+TotPromo)
		#sql="SELECT Count(TarifaPreferente),TarifaPreferente,Importe, Count(TarifaPreferente)*Importe as ImporteTot FROM Entradas where CorteInc > (%s-1) AND CorteInc < (%s+1) GROUP BY TarifaPreferente,Importe ORDER BY ImporteTot;"
		cursor.execute(sql,datos1)
		cone.close()
		return cursor.fetchall()   
 
####PENSIONADOS
	def ValidarRFID(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT id_cliente FROM Pensionados WHERE Num_tarjeta=%s"
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()       
	def AltaPensionado(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="INSERT INTO Pensionados(Num_tarjeta, Nom_cliente, Apell1_cliente, Apell2_cliente, Fecha_alta, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle_num, Placas, Modelo_auto, Color_auto, Monto, Cortesia, Tolerancia) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		#datos=(numtarjeta, Nombre, ApellidoPat, ApellidoMat, fechaAlta, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle, Placa, Modelo, Color, montoxmes, cortesia, tolerancia)
		cursor.execute(sql, datos)
		cone.commit()
		cone.close()
	def ConsultaPensionado(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT Nom_cliente, Apell1_cliente, Apell2_cliente, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle_num, Placas, Modelo_auto, Color_auto, Fecha_vigencia, Estatus, Vigencia, Monto, Cortesia, Tolerancia FROM Pensionados where id_cliente=%s"
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()
	def ModificarPensionado(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="UPDATE Pensionados SET Num_tarjeta=%s, Nom_cliente=%s, Apell1_cliente=%s, Apell2_cliente=%s, Telefono1=%s, Telefono2=%s, Ciudad=%s, Colonia=%s, CP=%s, Calle_num=%s, Placas=%s, Modelo_auto=%s, Color_auto=%s, Monto=%s, Cortesia=%s, Tolerancia=%s, Ult_Cambio=%s WHERE id_cliente=%s"
		#datos=(numtarjeta, Nombre, ApellidoPat, ApellidoMat, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle, Placa, Modelo,                    Color, montoxmes, cortesia, tolerancia, PensionadoOpen)
		cursor.execute(sql, datos)
		cone.commit()
		cone.close()
	def CobrosPensionado(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="INSERT INTO PagosPens(idcliente, num_tarjeta, Fecha_pago, Fecha_vigencia, Mensualidad, Monto, TipoPago) values (%s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(sql,datos)
		cone.commit()
		cone.close()
	def UpdPensionado(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="UPDATE Pensionados SET Vigencia=%s, Fecha_vigencia=%s WHERE id_cliente=%s"
		#sql = "update Entradas set CorteInc = %s, vobo = %s where TiempoTotal is not null and CorteInc=0;"
		cursor.execute(sql, datos)
		cone.commit()
		cone.close()
	def UpdMovsPens(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="UPDATE MovimientosPens SET Salida=%s, Estatus=%s WHERE idcliente=%s and Salida is null"
		#sql = "update Entradas set CorteInc = %s, vobo = %s where TiempoTotal is not null and CorteInc=0;"
		cursor.execute(sql, datos)
		cone.commit()
		cone.close()
	def UpdPens2(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="UPDATE Pensionados SET Estatus=%s WHERE id_cliente=%s"
		#sql = "update Entradas set CorteInc = %s, vobo = %s where TiempoTotal is not null and CorteInc=0;"
		cursor.execute(sql, datos)
		cone.commit()
		cone.close()
	def ValidarTarj(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT id_cliente, Estatus FROM Pensionados WHERE Num_tarjeta=%s"
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()
	def TreaPenAdentro(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="""SELECT Num_tarjeta, Nom_cliente, Apell1_cliente, Placas, Modelo_auto from Pensionados where Estatus = "Adentro";"""
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()      

#####USUARIOS###

	def ConsultaUsuario(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT Id_usuario, Contrasena, Nom_usuario FROM Usuarios WHERE Usuario = %s"
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall() 
	def CajeroenTurno(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT min(id_movs), nombre, inicio, turno, Idusuario FROM MovsUsuarios where CierreCorte is null"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()   
	def IniciosdeTurno(self, dato):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT inicio, usuario FROM MovsUsuarios where inicio > %s" #and CierreCorte = 'No aplica'  Idusuario = %s and 
		cursor.execute(sql, dato)
		cone.close()
		return cursor.fetchall()                 
	def ActuaizaUsuario(self, actual):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="INSERT INTO MovsUsuarios(Idusuario, usuario, inicio, nombre, turno) values (%s,%s,%s,%s,%s)"
		#sql="INSERT INTO PagosPens(idcliente, num_tarjeta, Fecha_pago, Fecha_vigencia, Mensualidad, Monto) values (%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql,actual)
		cone.commit()
		cone.close()
	def Cierreusuario(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update MovsUsuarios set CierreCorte = %s where  id_movs = %s;"
		cursor.execute(sql,datos)
		cone.commit()
		cone.close()
	def NoAplicausuario(self, dato):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update MovsUsuarios set CierreCorte = 'No aplica' where  id_movs > %s;"
		cursor.execute(sql,dato)        
		cone.commit()
		cone.close()    




	def nombre_usuario_activo(self):
		"""
		Esta función realiza una consulta a la base de datos para obtener el nombre del usuario que esta activo.
		Args:
		- self: referencia a la clase donde está definida la función.
		Returns:
		- resultados: lista de tuplas que contienen la siguiente información:
			- nombre: El nombre del usuario
		Esta función utiliza la librería de MySQL Connector para conectarse a la base de datos y ejecutar una consulta SQL.
		"""

		# Se establece la conexión con la base de datos.
		cone = self.abrir()

		# Se crea un cursor para ejecutar la consulta.
		cursor = cone.cursor()

		# Se define la consulta SQL.
		sql = f"""SELECT nombre FROM MovsUsuarios WHERE CierreCorte IS Null"""

		# Se ejecuta la consulta y se almacenan los resultados en una lista de tuplas.
		cursor.execute(sql)
		resultados = cursor.fetchall()

		# Se cierra la conexión con la base de datos.
		cone.close()

		# Se devuelve la lista de tuplas con los resultados de la consulta.
		return resultados

	def total_pensionados_corte(self, corte):
		"""
		Realiza una consulta a la base de datos para obtener la cantidad y el importe total de los pagos de pensiones 
		realizados en un corte específico.
		Args:
			self: referencia a la clase donde está definida la función.
			corte (int): el número de folio del corte que se desea consultar.
		Returns:
			resultados (list): una lista de tuplas que contienen la siguiente información:
				- Cuantos (int): la cantidad de pagos de pensiones realizados en el corte.
				- Concepto (str): una cadena que indica el tipo de pago (en este caso, siempre será "Pensionados").
				- ImporteTotal (float): el importe total de los pagos de pensiones realizados en el corte.
		Esta función utiliza la librería de MySQL Connector para conectarse a la base de datos y ejecutar una consulta SQL.
		"""
		# Se establece la conexión con la base de datos.
		cone = self.abrir()

		# Se crea un cursor para ejecutar la consulta.
		cursor = cone.cursor()

		# Se define la consulta SQL.
		sql = f"""SELECT COUNT(*) AS Cuantos, TipoPago AS Concepto, COALESCE(FORMAT(SUM(p.Monto), 2), 0) AS ImporteTotal FROM PagosPens p INNER JOIN Cortes c ON p.Fecha_pago BETWEEN c.FechaIni AND c.FechaFin WHERE c.Folio = {corte} GROUP BY TipoPago;"""

		# Se ejecuta la consulta y se almacenan los resultados en una lista de tuplas.
		cursor.execute(sql)
		resultados = cursor.fetchall()

		# Se cierra la conexión con la base de datos.
		cone.close()

		# Se devuelve la lista de tuplas con los resultados de la consulta.
		return resultados



	def cifrar_AES(self, texto_plano: str, clave: str = "PASE") -> tuple:
		"""
		Cifra un mensaje en texto plano utilizando el algoritmo de cifrado AES con una clave proporcionada.

		Args:
			texto_plano (str): El mensaje que se desea cifrar en texto plano.
			clave (str, opcional): La clave que se utilizará para cifrar el mensaje. Debe ser una cadena de caracteres ASCII.
				Por defecto es "PASE".

		Returns:
			tuple: Una tupla que contiene el texto cifrado y el vector de inicialización utilizado para cifrar el mensaje.
				El texto cifrado es una cadena de caracteres ASCII codificada en Base64, y el vector de inicialización es una cadena
				de bytes de 16 caracteres.

		Raises:
			TypeError: Si el argumento texto_plano no es una cadena de caracteres.
			TypeError: Si el argumento clave no es una cadena de caracteres.
			ValueError: Si la longitud de la clave proporcionada es mayor que 32 caracteres.

		"""
		try:
			# Convertir la clave en una clave de 32 caracteres
			clave_hash = hashlib.sha256(clave.encode()).digest()

			# Crear un objeto de cifrado AES
			cipher = AES.new(clave_hash, AES.MODE_CBC)

			# Cifrar el texto plano y convertirlo en una cadena de bytes
			texto_cifrado_bytes = cipher.encrypt(pad(texto_plano.encode(), AES.block_size))

			# Codificar la cadena de bytes en Base64
			texto_cifrado = base64.b64encode(texto_cifrado_bytes).decode()

			# Guardar el vector de inicialización
			iv = cipher.iv

			# Retornar el texto cifrado y el vector de inicialización
			return texto_cifrado, iv

		except TypeError as error:
			mb.showwarning("Error", f"El texto a decifrar no es una cadena de caracteres, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {error}")

		except ValueError as error:
			mb.showwarning("Error", f"la longitud de la clave proporcionada es mayor que 32 caracteres, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {error}")

		except Exception as e:
			mb.showwarning("Error", f"Ha ocurrido un error inesperado al codificar, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {e}")

	def descifrar_AES(self, texto_cifrado: str, iv: bytes, clave: str = "PASE") -> str:
		"""
		Descifra un mensaje cifrado en texto plano utilizando el algoritmo de cifrado AES con una clave y un vector de inicialización proporcionados.

		Args:
			texto_cifrado (str): El mensaje cifrado que se desea descifrar. Debe ser una cadena de caracteres ASCII codificada en Base64.
			iv (bytes): El vector de inicialización utilizado para cifrar el mensaje. Debe ser una cadena de bytes de 16 caracteres.
			clave (str, opcional): La clave que se utilizará para cifrar el mensaje. Debe ser una cadena de caracteres ASCII.
				Por defecto es "PASE".

		Returns:
			texto_descifrado (str): El texto descifrado en formato de cadena de caracteres ASCII.

		Raises:
			TypeError: Si el argumento texto_cifrado no es una cadena de caracteres.
			TypeError: Si el argumento iv no es una cadena de bytes.
			TypeError: Si el argumento clave no es una cadena de caracteres.
			ValueError: Si la longitud de la clave proporcionada es mayor que 32 caracteres.
			ValueError: Si la longitud del vector de inicialización proporcionado es diferente de 16 caracteres.
			ValueError: Si el mensaje cifrado no tiene una longitud válida.

		"""

		try:
			# Convertir la clave en una clave de 32 caracteres
			clave_hash = hashlib.sha256(clave.encode()).digest()

			# Decodificar el texto cifrado de Base64
			texto_cifrado_bytes = base64.b64decode(texto_cifrado)

			# Verificar la longitud del vector de inicialización
			if len(iv) != 16:
				raise ValueError("El vector de inicialización debe ser una cadena de bytes de 16 caracteres.")

			# Crear un objeto de descifrado AES
			cipher = AES.new(clave_hash, AES.MODE_CBC, iv)

			# Descifrar el texto cifrado y eliminar el relleno
			texto_descifrado_bytes = cipher.decrypt(texto_cifrado_bytes)
			texto_descifrado = unpad(texto_descifrado_bytes, AES.block_size).decode()

			# Retornar el texto descifrado
			return texto_descifrado

		except TypeError as error:
			mb.showwarning("Error", f"El texto a desifrar no es una cadena de caracteres, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {error}")

		except ValueError as error:
			mb.showwarning("Error", f"Ha ocurrido un error de valor, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {error}")

		except Exception as e:
			mb.showwarning("Error", f"Ha ocurrido un error inesperado al decodificar, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {e}")

	def generar_QR(self, QR_info: str, path: str = "reducida.png") -> None:
		"""Genera un código QR a partir de la información dada y lo guarda en un archivo de imagen.

		Args:
			QR_info (str): La información para generar el código QR.
			path (str, optional): La ruta y el nombre del archivo de imagen donde se guardará el código QR. 
								Por defecto es "reducida.png".
		"""
		# Generar el código QR
		img = qrcode.make(QR_info)

		# Redimensionar el código QR a un tamaño específico
		img = img.get_image().resize((350, 350))

		# Guardar la imagen redimensionada en un archivo
		img.save(path)

