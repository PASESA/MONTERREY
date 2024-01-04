import json


class ConfigController:
    def __init__(self) -> None:
        self.__json_path = r'Caseta\\Configuracion\\config.json'

    def get_config(self, type_config: str, module_config: str, name_config: str):
        try:
            with open(self.__json_path, encoding='utf-8') as f:
                data = json.load(f)
                return data[type_config][module_config][name_config]

        except FileNotFoundError:
            print(f'No se puede obtener configuracion')
            return

    def set_config(self, type_config: str, module_config: str, name_config: str, new_value):
        try:
            with open(self.__json_path, encoding='utf-8') as f:
                data = json.load(f)
                data[type_config][module_config][name_config] = new_value

        except FileNotFoundError:
            print(f'No se puede obtener configuracion')
            return


impresora = ConfigController().set_config(
    "general", "informacion_estacionamiento", "nombre_estacionamiento", "Durango")
print(impresora)
