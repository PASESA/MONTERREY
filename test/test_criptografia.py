import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import qrcode
from tkinter import messagebox as mb


def cifrar_AES(texto_plano: str, clave: str = "PASE") -> tuple:
    """
    Cifra un mensaje en texto plano utilizando el algoritmo de cifrado AES con una clave proporcionada.

    Args:
        texto_plano (str): El mensaje que se desea cifrar en texto plano.
        clave (str, opcional): La clave que se utilizará para cifrar el mensaje. Debe ser una cadena de caracteres ASCII.
            Por defecto es "PASE".

    Returns:
        tuple: Una tupla que contiene el texto cifrado y el vector de inicialización utilizado para cifrar el mensaje.
            texto_cifrado (str): Texto cifrado en Base64.
            iv (bytes): Vector de inicialización utilizado en el cifrado.

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

def descifrar_AES(texto_cifrado: str, iv: bytes, clave: str = "PASE") -> str:
    """
    Descifra un mensaje cifrado en texto plano utilizando el algoritmo de cifrado AES en modo CBC con una clave y un vector de inicialización proporcionados.

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

def generar_QR(QR_info: str, path: str = "reducida.png") -> None:
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


def test():
    #folio = "9999999999"
    folio = input("Ingresa el texto a codificar: ")

    texto_cifrado, iv = cifrar_AES(texto_plano = folio)

    imgqr = tuple((texto_cifrado, iv))

    generar_QR(imgqr)

    qr = input("Ingresa qr: ")
    # Convertir el string a una tupla
    imgqr = eval(qr)

    folio_cifrado = imgqr[0]
    vector = imgqr[1]

    texto_descifrado = descifrar_AES(texto_cifrado = folio_cifrado, iv = vector)

    print(f"\nFolio desifrado: {texto_descifrado}")

    if folio == texto_descifrado: print("\nDESIFRADO CORRECTO")
    else: print("\nCifrado incorrecto")

test()




