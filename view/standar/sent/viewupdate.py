import json

from PyQt5 import QtCore, QtWidgets
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


class Viewupdate(QtWidgets.QMainWindow):
    def __init__(
        self,
        uid,
        method,
        description,
        price_sent,
        status,
        country,
        region,
        commune,
        address_description,
    ):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainsentupdate{self.theme}.ui", self)

        set_default_size_and_center(self)
        icon_configurate_top(self)
        delete_banner(self)

        self.sale_total = 0.0

        self.uid = uid
        self.descriptiontxt.setText(description)
        self.pricesenttxt.setText(price_sent)

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

        self.controllersent = SentController(self)
        self.controlleraddress = AddressController(self)

        self.btn_update.clicked.connect(self.update)

        self.show_address(uid, country, region, commune, address_description)
        self.get_json_method(method)
        self.get_json_status(status)

    def show_address(self, uid, country, region, commune, address_description):
        # Desconectar la señal para evitar bucles infinitos
        self.address_combobox.blockSignals(True)

        self.address_combobox.clear()

        address = f"{country} - {region} - {commune} - {address_description}"

        self.address_combobox.addItem(address, uid)
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

    def get_json_method(self, method):
        try:
            # Abre el archivo JSON
            with open("json/method.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                methods = self.datos.get("shipping_methods", [])

                self.method_combobox.addItem(method)

                if not methods:
                    raise ValueError("No se encontraron datos en 'shipping_methods'")

                # Agregar los nombres de las regiones al QComboBox
                for method in methods:
                    self.method_combobox.addItem(method["name"])

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

    def get_json_status(self, status):
        try:
            # Abre el archivo JSON
            with open("json/status_send.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                status_send = self.datos.get("status", [])

                self.status_combobox.addItem(status)

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

    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__()  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana

    def update(self):
        address = self.address_combobox.currentData()
        method = self.method_combobox.currentText()
        description = self.descriptiontxt.toPlainText()
        price_send = self.pricesenttxt.text()
        status = self.status_combobox.currentText()

        if not method or not description or not price_send or not status:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controllersent.update(
            self.uid, address, method, description, price_send, status
        )
