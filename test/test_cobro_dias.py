from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta


import math

monto = 1000
dias_mes = 31

costo_x_dia = monto/dias_mes
dias = dias_mes - 13
pago = costo_x_dia * dias
print (pago)



def calcular_pago(monto):
    mes_actual = 7
    año_actual = 2023

    ultimo_dia_mes = date(año_actual, mes_actual, 1) + relativedelta(day=31)
    dias_mes = ultimo_dia_mes.day

    dias_faltantes = dias_mes - date.today().day
    pago = math.ceil((monto / dias_mes) * dias_faltantes)

    return pago



print(calcular_pago(monto))

