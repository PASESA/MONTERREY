



def Comprobante(self, titulo:str = 'Comprobante de pago', imagen_logo:bool = True, QR_salida:bool = False):

    Placa = self.Placa.get()
    Folio = self.folio.get()
    TipoPromo = self.PrTi.get()
    Importe = self.importe.get()
    Entrada = str(self.descripcion.get())[:-3]
    Salio = str(self.copia.get())[:-3]
    Tiempo = str(self.ffeecha.get())[:-3]

    valor = 'N/A'

    ###-###p.set(align="center")
    print(""+f"{titulo}\n")

    if Placa == "BoletoPerdido":
        Entrada = valor
        Salio = valor
        Tiempo = valor


    if imagen_logo:
        ###-###p.image(logo_1)
        print("Imprime logo")


    ###-###p.set(align="left")

    print(""+"El importe es: $" + Importe + "\n")
    print(""+'El auto entro: ' + Entrada + '\n')
    print(""+'El auto salio: ' + Salio + '\n')
    print(""+'El auto permanecio: ' + Tiempo + '\n')
    print(""+'El folio del boleto es: ' + Folio + '\n')
    print(""+'TIPO DE COBRO: ' + TipoPromo + '\n')

    if QR_salida:
        ###-###p.image(qr_imagen)
        print("Imprime QR salida")

    print(""+"----------------------------\n")

    ###-###p.cut()









