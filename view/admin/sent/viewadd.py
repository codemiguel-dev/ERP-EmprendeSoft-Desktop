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
from controller.controllersent import SentController


class Viewadd(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewadd, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainsentadd{self.theme}.ui", self)

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

        self.controller = SentController(self)
        self.controlleraddress = AddressController(self)

        self.show_address()
        self.get_json_method()
        self.get_json_status()

        self.btn_add.clicked.connect(self.register)

    def show_address(self):
        # Desconectar la señal para evitar bucles infinitos
        self.address_combobox.blockSignals(True)

        self.address_combobox.clear()
        # Obtener datos de inventario desde el controlador
        address = self.controlleraddress.get()

        # Añadir datos al comboBox
        for a in address:
            uid = a[0]  # El primer elemento es el ID del producto
            country = a[1]  # El segundo elemento es el país
            region = a[2]  # El tercer elemento es la región
            commune = a[3]
            description = a[4]

            # Concatenar country y region en una sola cadena
            address_str = f"{country} - {region} - {commune} - {description}"

            # Añadir la concatenación de country y region al combobox
            self.address_combobox.addItem(address_str, uid)

        # Reconectar la señal después de añadir los datos
        self.address_combobox.blockSignals(False)

    def get_json_method(self):
        try:
            # Abre el archivo JSON
            with open("json/method.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                regiones = self.datos.get("shipping_methods", [])

                if not regiones:
                    raise ValueError("No se encontraron datos en 'shipping_methods'")

                # Agregar los nombres de las regiones al QComboBox
                for region in regiones:
                    self.method_combobox.addItem(region["name"])

                # Conectar la señal de cambio de región
                # self.region_combobox.currentIndexChanged.connect(self.cargar_datos_json_commune)

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Archivo JSON no encontrado.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(
                self, "Error de JSON", f"Error al decodificar el archivo JSON: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {str(e)}")

    def get_json_status(self):
        try:
            # Abre el archivo JSON
            with open("json/status_send.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                status_send = self.datos.get("status", [])

                if not status_send:
                    raise ValueError("No se encontraron datos en 'shipping_methods'")

                # Agregar los nombres de las regiones al QComboBox
                for statuss in status_send:
                    self.status_combobox.addItem(statuss["name"])

                # Conectar la señal de cambio de región
                # self.region_combobox.currentIndexChanged.connect(self.cargar_datos_json_commune)

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Archivo JSON no encontrado.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(
                self, "Error de JSON", f"Error al decodificar el archivo JSON: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {str(e)}")

    def register(self):
        address = self.address_combobox.currentData()
        method = self.method_combobox.currentText()
        description = self.descriptiontxt.toPlainText()
        budget = self.budgettxt.text()
        status = self.status_combobox.currentText()

        if not address or not description or not budget or not status:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.register(address, method, description, budget, status)
