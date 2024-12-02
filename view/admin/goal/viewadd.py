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
from controller.controllerbusiness import BusinessController
from controller.controllergoal import GoalController


class Viewadd(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewadd, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/maingoaladd{self.theme}.ui", self)

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

        self.controller = GoalController(self)
        self.controllerbusiness = BusinessController(self)

        self.show_business()

        self.btn_add.clicked.connect(self.register)

        # self.cargar_datos_json_regions()

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
        business = self.business_combobox.currentData()
        name = self.nametxt.text()
        description = self.descriptiontxt.toPlainText()
        status = self.status_combobox.currentText()
        start_date = self.start_datetxt.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_datetxt.selectedDate().toString("yyyy-MM-dd")

        if not business or not name or not description or not status:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.register(
            business, name, description, status, start_date, end_date
        )

    def show_business(self):
        # Desconectar la señal para evitar bucles infinitos
        self.business_combobox.blockSignals(True)

        self.business_combobox.clear()
        # Obtener datos de inventario desde el controlador
        businesss = self.controllerbusiness.get()

        # Añadir productos al comboBox
        for business in businesss:
            uid = business[0]  # El primer elemento es el ID del producto
            name = business[1]  # El segundo elemento es el nombre del producto

            # Añadir el producto al combobox
            self.business_combobox.addItem(name, uid)

        # Reconectar la señal después de añadir los productos
        self.business_combobox.blockSignals(False)
