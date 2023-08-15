import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import requests
from requests.exceptions import RequestException

import traceback

from  zipfile import ZipFile, ZIP_DEFLATED
from os import path

class ToolsEmail:
    def check_internet_connection(self, url: str = "http://www.google.com", timeout: int = 5) -> bool:
        """
        Comprueba si hay una conexión activa a Internet mediante la realización de una petición HTTP a la URL dada.

        Args:
            url (str, optional): La URL a la que se realizará la petición. Por defecto es "http://www.google.com".
            timeout (int, optional): El tiempo máximo en segundos para esperar la respuesta. Por defecto es 5.

        Returns:
            bool: True si hay una conexión activa a Internet, False si no se puede establecer la conexión.
        """
        try:
            response = requests.get(url, timeout=timeout)
            # Lanza una excepción si la respuesta HTTP no es exitosa
            response.raise_for_status()
            print("Conexión a Internet activa.")
            return True

        except RequestException:
            print("No se pudo establecer conexión a Internet.")
            traceback.print_exc()
            return False

class SendEmail:
    def __init__(self, username: str, password: str, estacionamiento: str, smtp_server: str = "smtp.pasesa.com.mx", smtp_port: int = 1025) -> None:
        """
        Inicializa una instancia de la clase SendEmail para enviar correos electrónicos con archivos adjuntos.

        Args:
            username (str): El nombre de usuario para la cuenta de correo electrónico.
            password (str): La contraseña para la cuenta de correo electrónico.
            estacionamiento (str): Nombre del estacionamiento, utilizado en el nombre del archivo adjunto.
            smtp_server (str, opcional): El servidor SMTP para el envío de correos. Por defecto es "smtp.pasesa.com.mx".
            smtp_port (int, opcional): El puerto del servidor SMTP. Por defecto es 1025.
        """
        self.username = username
        self.password = password
        self.estacionamiento = estacionamiento
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.tools = ToolsEmail()

    def send_mail(self, to_email: str, subject: str, message: str, file: str) -> bool:
        """
        Envía un correo electrónico con un archivo adjunto.

        Args:
            to_email (str): La dirección de correo electrónico del destinatario.
            subject (str): El asunto del correo electrónico.
            message (str): El contenido del correo electrónico.
            file (str): Ruta al archivo que se adjuntará al correo.

        Returns:
            bool: True si el correo se envía exitosamente, False si hay algún error.
        """
        from_email = self.username

        # Verificar la conexión a Internet antes de intentar enviar el correo
        if self.tools.check_internet_connection() == False:
            return False
        else:
            try:
                #Crea la estructura del correo
                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))

                zip_file = self.compress_file_to_zip(file)

                # Adjuntar el archivo al correo
                with open(zip_file, 'rb') as f:
                    attached_file = MIMEApplication(f.read(), _subtype="zip")
                    attached_file.add_header('content-disposition', 'attachment', filename=f'{self.estacionamiento}_DB.zip')
                    msg.attach(attached_file)

                # Conectar al servidor SMTP y enviar el correo
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    # Iniciar la conexión segura TLS
                    server.starttls()
                    # Inicio de sesion
                    server.login(self.username, self.password)
                    # Envia correo
                    server.sendmail(from_email, to_email, msg.as_string())
                    # Termina la sesión
                    server.quit()


                print('Correo enviado exitosamente.')
                return True

            except Exception as e:
                print(e)
                traceback.print_exc()
                return False

    def compress_file_to_zip(self, source_file: str, output_filename: str = None) -> str or None:
        """
        Comprime un archivo en un archivo ZIP.

        Args:
            source_file (str): Ruta al archivo que se comprimirá.
            output_filename (str): Nombre del archivo ZIP de salida. Si no se proporciona, se usará el nombre del archivo fuente con extensión ".zip".

        Returns:
            str or None: Ruta absoluta del archivo ZIP si la compresión es exitosa, None si hay algún error.
        """
        try:
            if output_filename is None:
                # Si no se proporciona un nombre de archivo de salida, usamos el nombre del archivo fuente con extensión ".zip"
                output_filename = source_file + '.zip'

            with ZipFile(output_filename, 'w', ZIP_DEFLATED) as zipf:
                arcname = path.basename(source_file)
                zipf.write(source_file, arcname)
                absolute_path_zip = path.abspath(output_filename)
                print("Archivo comprimido correctamente")
                return absolute_path_zip

        except Exception as e:
            print(f'Error al comprimir el archivo: {e}')
            return None