from datetime import datetime, timedelta
import math

# Obtener la fecha y hora actual en formato deseado
# hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hoy = '2023-07-30 11:59:59' 
hoy = datetime.strptime(hoy, "%Y-%m-%d %H:%M:%S")


# # Penalización diaria en dinero
# penalizacion_diaria = 1

# # Fecha de vigencia en formato YYYY-MM-DD HH:MM:SS (último día de un mes)
fecha_limite = "2023-07-03 23:59:59"
fecha_limite = datetime.strptime(fecha_limite, "%Y-%m-%d %H:%M:%S") + timedelta(days=5)


print(f"fecha actual: {hoy}")


fecha = hoy - fecha_limite
print(f"fecha limite: {fecha_limite}")


print(f"Diferencia: {fecha}")

fecha_limite = (hoy - fecha_limite).days
print(fecha_limite)




