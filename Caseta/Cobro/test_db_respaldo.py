import os
import subprocess
from operacion import Operacion

DB = Operacion()


def get_DB(backup_path:str = '/ruta/de/respaldo/Parqueadero1.sql'):
    # Configuración de la base de datos
    host = DB.host
    user = DB.user
    password = DB.password
    database = DB.database

    # Comando mysqldump
    command = f"mysqldump -h {host} -u {user} -p{password} {database} > {backup_path}"

    try:
        subprocess.run(command, shell=True, check=True)

        # Verifica si el archivo de respaldo existe
        if os.path.exists(backup_path):
            print("Respaldo creado exitosamente.")
            print(f"El archivo de respaldo se encuentra en: {backup_path}")
            return backup_path
        else:
            print("El archivo de respaldo no se creó correctamente.")
            return None

    except subprocess.CalledProcessError:
        print("Error al crear el respaldo.")
        return None

a = DB.MaxfolioEntrada()
a = a[0][0]


print(a)



