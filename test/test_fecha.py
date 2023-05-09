from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from tkinter import messagebox as mb

# Obtener la fecha y hora actual en formato deseado
fecha = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

fecha = "2023-04-30 23:59:59"

# Convertir la cadena de caracteres en un objeto datetime
fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")


def nueva_vigencia(fecha):
    """
    Obtiene la fecha del último día del mes siguiente a la fecha dada y la devuelve como una cadena de texto en el formato '%Y-%m-%d %H:%M:%S'.

    :param fecha (str or datetime): Fecha a partir de la cual se obtendrá la fecha del último día del mes siguiente.

    :raises: TypeError si la fecha no es una cadena de texto ni un objeto datetime.

    :return:
        - nueva_vigencia (str): Una cadena de texto en el formato '%Y-%m-%d %H:%M:%S' que representa la fecha del último día del mes siguiente a la fecha dada.
    """
    try:
        # Verificar que la fecha sea de tipo str o datetime
        if not isinstance(fecha, (str, datetime)):
            raise TypeError("La fecha debe ser una cadena de texto o un objeto datetime.")
        
        # Convertir la fecha dada en un objeto datetime si es de tipo str
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        
        # Obtener la fecha del primer día del siguiente mes
        mes_siguiente = fecha + relativedelta(months=1, day=1)
        
        # Obtener la fecha del último día del mes siguiente
        ultimo_dia_mes_siguiente = mes_siguiente + relativedelta(day=31)
        if ultimo_dia_mes_siguiente.month != mes_siguiente.month:
            ultimo_dia_mes_siguiente -= relativedelta(days=1)
        
        # convertir la fecha del último día del mes siguiente en formato de cadena
        nueva_vigencia = ultimo_dia_mes_siguiente.strftime('%Y-%m-%d %H:%M:%S')

        # Devolver el valor
        return nueva_vigencia
    
    except TypeError as e:
        mb.showwarning("Error", f"{e}")
    except Exception as e:
        mb.showwarning("Error", f"{e}")


Tolerancia = 5
# Obtener la fecha y hora actual en formato deseado
VigAct = "2023-05-31 23:59:59"
# Convertir la cadena de caracteres en un objeto datetime
VigAct = datetime.strptime(VigAct, "%Y-%m-%d %H:%M:%S")

# Obtener la fecha y hora actual en formato deseado
hoy = "2023-06-5 23:59:8"
# Convertir la cadena de caracteres en un objeto datetime
hoy = datetime.strptime(hoy, "%Y-%m-%d %H:%M:%S")

limite = VigAct + timedelta(days=Tolerancia)

print(f"Hoy     : {hoy}")
print(f"Vigencia: {limite}")


if hoy >= limite:
        print("No vigente")
else:
    print("------------------")
    print("Aun hay tolerancia")

