import random
import qrcode
from tkinter import messagebox as mb

def cifrar_folio(folio):
	"""
	Cifra un número de folio utilizando una tabla de sustitución numérica.

	Args:
		folio (int): Número de folio a cifrar.

	Returns:
		str: Número de folio cifrado.
	"""

	# Convierte el número de folio en una cadena de texto.
	folio = str(folio)

	# Genera un número aleatorio de 5 dígitos y lo convierte en una cadena de texto.
	num_random = random.randint(10000, 99999)
	numero_seguridad = str(num_random)

	# Concatena el número de seguridad al número de folio.
	folio = folio + numero_seguridad

	# Imprime el número de folio cifrado (sólo para propósitos de depuración).
	print(folio)

	# Tabla de sustitución numérica.
	tabla = {'0': '5', '1': '3', '2': '9', '3': '1', '4': '7', '5': '0', '6': '8', '7': '4', '8': '6', '9': '2'}

	# Convierte el número de folio cifrado a una lista de dígitos.
	digitos = list(folio)

	# Sustituye cada dígito por el número correspondiente en la tabla de sustitución.
	cifrado = [tabla[digito] for digito in digitos]

	# Convierte la lista cifrada de vuelta a una cadena de texto.
	cifrado = ''.join(cifrado)

	# Devuelve el número de folio cifrado.
	return cifrado


def descifrar_folio(folio_cifrado):
	"""
	Descifra un número de folio cifrado utilizando una tabla de sustitución numérica.

	Args:
		folio_cifrado (str): Número de folio cifrado.

	Returns:
		str: Número de folio descifrado.
	"""
	try:
		# Verifica si el número de folio es válido.
		if len(folio_cifrado) <= 5:
			raise ValueError("El folio no es válido, escanee nuevamente, si el error persiste contacte con un administrador.")

		# Verifica si el número de folio tiene caracteres inválidos.
		caracteres_invalidos = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '{', '}', '[', ']', '|', '\\', ':', ';', '<', '>', ',', '.', '/', '?']
		if any(caracter in folio_cifrado for caracter in caracteres_invalidos):
			raise TypeError("El folio no tiene un formato válido")

		# Tabla de sustitución numérica.
		tabla = {'0': '5', '1': '3', '2': '9', '3': '1', '4': '7', '5': '0', '6': '8', '7': '4', '8': '6', '9': '2'}

		# Convierte el número de folio cifrado a una lista de dígitos.
		digitos_cifrados = list(folio_cifrado)

		# Crea una tabla de sustitución inversa invirtiendo la tabla original.
		tabla_inversa = {valor: clave for clave, valor in tabla.items()}

		# Sustituye cada dígito cifrado por el número correspondiente en la tabla de sustitución inversa.
		descifrado = [tabla_inversa[digito] for digito in digitos_cifrados]

		# Convierte la lista descifrada de vuelta a una cadena de texto.
		descifrado = ''.join(descifrado)

		# Elimina los últimos 4 dígitos, que corresponden al número aleatorio generado en la función cifrar_folio.
		descifrado = descifrado[:-5]

		# Retorna el folio descifrado.
		return descifrado

	# Maneja el error si el formato del número de folio es incorrecto.
	except TypeError as error:
		mb.showerror("Error", f"El folio tiene un formato incorrecto, si el error persiste contacte a un administrador y muestre el siguiente error:\n{error}")
		return None

	# Maneja cualquier otro error que pueda ocurrir al descifrar el número de folio.
	except Exception as error:
		mb.showerror("Error", f"Ha ocurrido un error al descifrar el folio, intente nuevamente, si el error persiste contacte a un administrador y muestre el siguiente error:\n{error}")
		return None


def generar_QR(QR_info: str, path: str = "reducida.png") -> None:
	"""Genera un código QR a partir de la información dada y lo guarda en un archivo de imagen.

	Args:
		QR_info (str): La información para generar el código QR.
		path (str, optional): La ruta y el nombre del archivo de imagen donde se guardará el código QR, por defecto es "reducida.png".
	"""
	# Generar el código QR
	img = qrcode.make(QR_info)

	# Redimensionar el código QR a un tamaño específico
	img = img.get_image().resize((320, 320))

	# Guardar la imagen redimensionada en un archivo
	img.save(path)

