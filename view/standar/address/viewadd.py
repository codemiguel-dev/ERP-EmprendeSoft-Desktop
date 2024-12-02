import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QSizeGrip
from PyQt5.uic import loadUi

from configuration.configuration_buttom import icon_configurate_top
from configuration.configuration_buttom_top import (
    control_bt_maximizar,
    control_bt_minimizar,
    control_bt_normal,
)
from configuration.configuration_config_theme import load_config
from configuration.configuration_delete_banner import delete_banner
from configuration.configuration_size_window import set_default_size_and_center
from configuration.configuration_window_move import mousePressEvent, window_move
from controller.controlleraddress import AddressController
from controller.controlleruser import UserController


class Viewadd(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewadd, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainaddressadd{self.theme}.ui", self)

        set_default_size_and_center(self)
        icon_configurate_top(self)
        delete_banner(self)

        # Inicializar el QSizeGrip y establecer su tamaño
        self.gripSize = 16  # Define el tamaño del grip
        self.grip = QSizeGrip(self)  # Crea un QSizeGrip para el redimensionamiento
        self.grip.resize(self.gripSize, self.gripSize)  # Ajusta el tamaño del QSizeGrip

        # Asigna los eventos personalizados al frame superior
        self.frame_superior.mousePressEvent = lambda event: mousePressEvent(self, event)
        self.frame_superior.mouseMoveEvent = lambda event: window_move(self, event)

        # Control de botones de la barra de títulos
        self.bt_minimizar.clicked.connect(lambda: control_bt_minimizar(self))

        self.bt_restaurar.clicked.connect(lambda: control_bt_normal(self))
        self.bt_maximizar.clicked.connect(lambda: control_bt_maximizar(self))
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_restaurar.hide()

        self.controller = AddressController(self)
        self.controlleruser = UserController(self)

        # self.show_user()

        self.btn_add.clicked.connect(self.register)
        # self.btn_address.clicked.connect(self.address)

        self.cargar_datos_json_regions()
        self.cargar_datos_json_commune()

    def cargar_datos_json_regions(self):
        try:
            # Abre el archivo JSON
            with open("json/address.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                regiones = self.datos.get("regions", [])

                if not regiones:
                    raise ValueError("No se encontraron datos en 'regions'")

                # Agregar los nombres de las regiones al QComboBox
                for region in regiones:
                    self.region_combobox.addItem(region["name"])

                # Conectar la señal de cambio de región
                self.region_combobox.currentIndexChanged.connect(
                    self.cargar_datos_json_commune
                )

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Archivo JSON no encontrado.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(
                self, "Error de JSON", f"Error al decodificar el archivo JSON: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {str(e)}")

    def cargar_datos_json_commune(self):
        # Obtener el índice seleccionado del QComboBox de regiones
        region_seleccionada = self.region_combobox.currentText()

        # Limpiar el QComboBox de comunas antes de cargar nuevos valores
        self.commune_combobox.clear()

        # Buscar la región seleccionada en los datos JSON
        for region in self.datos.get("regions", []):
            if region["name"] == region_seleccionada:
                # Si se encuentra la región, cargar sus comunas en el QComboBox
                for commune in region.get("communes", []):
                    self.commune_combobox.addItem(commune["name"])
                break  # Salir del bucle una vez que se encuentran las comunas

    def register(self):
        country = "Chile"
        region = self.region_combobox.currentText()
        commune = self.commune_combobox.currentText()
        description = self.descriptiontxt.text()

        if not region or not commune or not description:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.register(country, region, commune, description)

    def show_user(self):
        # Desconectar la señal para evitar bucles infinitos
        self.user_combobox.blockSignals(True)

        self.user_combobox.clear()
        # Obtener datos de inventario desde el controlador
        users = self.controlleruser.get_user()

        # Añadir productos al comboBox
        for client in users:
            uid = client[0]  # El primer elemento es el ID del producto
            name = client[2]  # El segundo elemento es el nombre del producto

            # Añadir el producto al combobox
            self.user_combobox.addItem(name, uid)

        # Reconectar la señal después de añadir los productos
        self.user_combobox.blockSignals(False)

    # def address(self):
    #    self.view_address = Viewmainaddress()
    #    self.view_address.show()
