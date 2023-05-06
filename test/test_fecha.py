from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from tkinter import messagebox as mb

# Obtener la fecha y hora actual en formato deseado
fecha = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

fecha = "2023-04-30 23:59:59"

# Convertir la cadena de caracteres en un objeto datetime
fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")


def nueva_vigencia(fecha):
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
    
    # Devolver la fecha del último día del mes siguiente en formato de cadena
    return ultimo_dia_mes_siguiente.strftime('%Y-%m-%d %H:%M:%S')





print(nueva_vigencia(fecha))
