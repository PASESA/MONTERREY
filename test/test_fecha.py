from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from tkinter import messagebox as mb
import traceback

def nueva_vigencia(fecha, meses = 1, cortesia = None):
    """
    Obtiene la fecha del último día del mes siguiente a la fecha dada y la devuelve como una cadena de texto en el formato '%Y-%m-%d %H:%M:%S'.

    :param fecha (str or datetime): Fecha a partir de la cual se obtendrá la fecha del último día del mes siguiente.

    :raises: TypeError si la fecha no es una cadena de texto ni un objeto datetime.

    :return:
        - nueva_vigencia (str): Una cadena de texto en el formato '%Y-%m-%d %H:%M:%S' que representa la fecha del último día del mes siguiente a la fecha dada.
    """
    try:
        nueva_vigencia = ''
        if fecha == None:
            # Obtener la fecha y hora actual en formato deseado
            fecha = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

            # fecha = "2023-04-30 23:59:59"

            # Convertir la cadena de caracteres en un objeto datetime
            fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")

            fecha = fecha - relativedelta(months=1)

        # Verificar que la fecha sea de tipo str o datetime
        elif not isinstance(fecha, (str, datetime)):
            raise TypeError("La fecha debe ser una cadena de texto o un objeto datetime.")

        # Convertir la fecha dada en un objeto datetime si es de tipo str
        elif isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d 23:59:59')

        if cortesia == "Si":
            nueva_vigencia = fecha + relativedelta(years=1)

        else:
            # Obtener la fecha del primer día del siguiente mes
            mes_siguiente = fecha + relativedelta(months=meses, day=1)
            
            # Obtener la fecha del último día del mes siguiente
            ultimo_dia_mes_siguiente = mes_siguiente + relativedelta(day=31)
            if ultimo_dia_mes_siguiente.month != mes_siguiente.month:
                ultimo_dia_mes_siguiente -= relativedelta(days=1)

            nueva_vigencia = ultimo_dia_mes_siguiente

        # convertir la fecha en formato de cadena
        nueva_vigencia = nueva_vigencia.strftime('%Y-%m-%d 23:59:59')

        # Devolver el valor
        return nueva_vigencia
    
    except TypeError as e:
        print(e)
        traceback.print_exc()
        mb.showwarning("Error", f"{e}")
    except Exception as e:
        print(e)
        traceback.print_exc()
        mb.showwarning("Error", f"{e}")


fecha = "2024-01-31 14:38:27"

# Convertir la cadena de caracteres en un objeto datetime
fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")


print(f"{fecha}\n")  



nueva_fecha = nueva_vigencia(fecha, 1)
print(nueva_fecha)  

