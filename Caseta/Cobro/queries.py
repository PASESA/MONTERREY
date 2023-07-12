import re
from pymysql import err
from tkinter import messagebox
from operacion import Operacion

class usuarios:

    def __init__ (self):
        operacion = Operacion()
        self.connection = operacion.abrir()

    def execute_query(self, query: str):
        """
        Ejecuta una consulta en la base de datos.

        :param query (str): La consulta SQL a ejecutar.

        :raises pymysql.err.OperationalError: Si la conexion se pierde.
        :raises err.ProgrammingError: Si la tabla no existe.

        :return:
            - result (list): Una lista con los resultados de la consulta.
        """
        try:
            if self.connection:
                # Crea un objeto cursor para ejecutar la consulta
                self.cursor = self.connection.cursor()

                # Se ejecuta la consulta
                self.cursor.execute(query)

                # Obtiene los resultados de la consulta
                result = self.cursor.fetchall()

                # Confirma los cambios en la base de datos
                self.connection.commit()

                # Cierra el cursor
                self.cursor.close()

                # Retorna los resultados de la consulta
                return result

        except err.OperationalError as e:
            if "10054" in str(e):
                print(e)
                messagebox.showwarning("Error", "Se ha perdido la conexión con el servidor.\nEl programa se cerrará, posterior a eso inicie nuevamente sesión\n\nEn caso de que el error persista contacte a un administrador.")

        except err.ProgrammingError as error:
            # Aquí se ejecuta el código en caso de que se genere la excepción ProgrammingError
            error_message = str(error)
            match = re.search(r"\((\d+),", error_message)
            error_number = int(match.group(1))
            if error_number == 1146:
                print(error)
                messagebox.showwarning("Error", f"Error: La tabla no existe.\n Es probable que la conexion actual no cuente con la tabla a la que intenta acceder, de ser caso contrario contacte con un administrador.")
                return None

        except Exception as e:
            print(e)
            messagebox.showwarning("Error", f"Error al realizar la consulta, por favor contacte con un administrador y muestre el siguiente error:\n Error: {str(e)} ")
            return None


    def agregar_usuarios(self, datos):
        datos = tuple(datos)

        if self.connection:

            query = f"INSERT INTO Usuarios (Usuario, Contrasena, Nom_usuario, Fecha_alta, Telefono1, TelefonoEmer, Sucursal) VALUES {datos};"

            # Se ejecuta la consulta
            self.execute_query(query)

    def consultar_usuario(self, id):
        if self.connection:

            query = f"SELECT Usuario, Contrasena, Nom_usuario, Telefono1, TelefonoEmer, Sucursal FROM Usuarios WHERE Id_usuario = {id}"

            # Se ejecuta la consulta y se obtiene el resultado.
            resultado = self.execute_query(query)

            return resultado

    def ver_usuarios(self):

        if self.connection:

            query = f"SELECT Id_usuario, Usuario, Nom_usuario, Fecha_alta, Telefono1, TelefonoEmer, Sucursal FROM Usuarios"

            # Se ejecuta la consulta y se obtiene el resultado.
            resultado = self.execute_query(query)

            return resultado

    def eliminar_usuario(self, id):

        if self.connection:

            query = f"DELETE FROM Usuarios WHERE Id_usuario = {id}"

            # Se ejecuta la consulta
            self.execute_query(query)

    def actualizar_usuarios(self, datos, id):

        if self.connection:
            datos = tuple(datos)
        
            query = f"UPDATE Usuarios SET Usuario = '{datos[0]}', Contrasena = '{datos[1]}', Nom_usuario = '{datos[2]}',  Telefono1 = '{datos[3]}', TelefonoEmer = '{datos[4]}', Sucursal = '{datos[5]}' WHERE Id_usuario = '{id}';"

            # Se ejecuta la consulta
            self.execute_query(query)

class pensionados(usuarios):

    def agregar_pensionados(self, datos):
        datos = tuple(datos)

        if self.connection:

            query = f"INSERT INTO Pensionados (Num_tarjeta, Nom_cliente, Apell1_cliente, Apell2_cliente, Fecha_alta, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle_num, Placas, Modelo_auto, Color_auto, Monto, Cortesia, Tolerancia) VALUES {datos};"

            # Se ejecuta la consulta
            self.execute_query(query)

    def consultar_pensionado(self, Num_tarjeta):
        if self.connection:
            query = f"SELECT Nom_cliente, Apell1_cliente, Apell2_cliente, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle_num, Placas, Modelo_auto, Color_auto, Fecha_vigencia, Estatus, Vigencia, Monto, Cortesia, Tolerancia FROM Pensionados WHERE Num_tarjeta = {Num_tarjeta}"

            # Se ejecuta la consulta y se obtiene el resultado.
            resultado = self.execute_query(query)

            return resultado

    def ver_pensionados(self):
        if self.connection:
            query = f"SELECT Num_tarjeta, Cortesia, Nom_cliente, Estatus, Fecha_vigencia, Tolerancia, Id_cliente FROM Pensionados ORDER BY Id_cliente DESC"

            # Se ejecuta la consulta y se obtiene el resultado.
            resultado = self.execute_query(query)

            return resultado

    def eliminar_pensinado(self, id):
        if self.connection:
            query = f"DELETE FROM Usuarios WHERE Id_usuario = {id}"

            # Se ejecuta la consulta
            self.execute_query(query)

    def actualizar_pensionado(self, datos, id):
        datos = tuple(datos)
    
        query = f"UPDATE Usuarios SET Usuario = '{datos[0]}', Contrasena = '{datos[1]}', Nom_usuario = '{datos[2]}',  Telefono1 = '{datos[3]}', TelefonoEmer = '{datos[4]}', Sucursal = '{datos[5]}' WHERE Id_usuario = '{id}';"

        # Se ejecuta la consulta
        self.execute_query(query)


    def ValidarRFID(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="SELECT id_cliente FROM Pensionados WHERE Num_tarjeta=%s"
        cursor.execute(sql,datos)
        cone.close()
        return cursor.fetchall()       
    def AltaPensionado(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="INSERT INTO Pensionados(Num_tarjeta, Nom_cliente, Apell1_cliente, Apell2_cliente, Fecha_alta, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle_num, Placas, Modelo_auto, Color_auto, Monto, Cortesia, Tolerancia) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #datos=(numtarjeta, Nombre, ApellidoPat, ApellidoMat, fechaAlta, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle, Placa, Modelo, Color, montoxmes, cortesia, tolerancia)
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()
    def ConsultaPensionado(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="SELECT Nom_cliente, Apell1_cliente, Apell2_cliente, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle_num, Placas, Modelo_auto, Color_auto, Fecha_vigencia, Estatus, Vigencia, Monto, Cortesia, Tolerancia FROM Pensionados where id_cliente=%s"
        cursor.execute(sql,datos)
        cone.close()
        return cursor.fetchall()
    def ModificarPensionado(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="UPDATE Pensionados SET Num_tarjeta=%s, Nom_cliente=%s, Apell1_cliente=%s, Apell2_cliente=%s, Telefono1=%s, Telefono2=%s, Ciudad=%s, Colonia=%s, CP=%s, Calle_num=%s, Placas=%s, Modelo_auto=%s, Color_auto=%s, Monto=%s, Cortesia=%s, Tolerancia=%s, Ult_Cambio=%s WHERE id_cliente=%s"
        #datos=(numtarjeta, Nombre, ApellidoPat, ApellidoMat, Telefono1, Telefono2, Ciudad, Colonia, CP, Calle, Placa, Modelo,                    Color, montoxmes, cortesia, tolerancia, PensionadoOpen)
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()