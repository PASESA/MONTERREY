import json


class ConfigController:
    def __init__(self) -> None:
        self.__json_path = r'Caseta\\Configuracion\\config.json'

    def get_config(self, *args: tuple):
        try:
            with open(self.__json_path, encoding='utf-8') as f:
                data = json.load(f)

                # Acceder a la información en función de los argumentos proporcionados
                current_data = data
                for arg in args:
                    current_data = current_data[arg]

                return current_data

        except FileNotFoundError:
            print('No se puede obtener configuracion')
            return
        except Exception as e:
            print(e)

    def set_config(self, *args: tuple, new_value):
        try:
            with open(self.__json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Acceder y actualizar la información en función de los argumentos proporcionados
            current_data = data
            for arg in args[:-1]:
                current_data = current_data[arg]
            current_data[args[-1]] = new_value

            # Guardar los cambios en el archivo
            with open(self.__json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            print('No se puede guardar configuracion')
        except Exception as e:
            print(e)

impresora = ConfigController().set_config(
    "funcionamiento_interno", "db", "usuario",  new_value="Noe")
print(impresora)
