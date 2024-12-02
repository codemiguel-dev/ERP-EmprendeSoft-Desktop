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
from controller.controllerinvestment import InvestmentController


class Viewadd(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewadd, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/maininvestmentadd{self.theme}.ui", self)

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

        self.controller = InvestmentController(self)

        self.btn_add.clicked.connect(self.register)
        self.btn_calculate_yield.clicked.connect(self.calculate_yield)

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
                break  # Salir del bucle una vez que se encuentran las comuna

    def calculate_yield(self):
        try:
            # Obtener los valores desde los campos de texto
            amount = float(self.amounttxt.text())  # Valor inicial
            amount_end = float(self.amount_endtxt.text())  # Valor final

            # Calcular el rendimiento
            yields = ((amount_end - amount) / amount) * 100

            # Mostrar el rendimiento calculado en el campo de texto yieldtxt
            self.yieldtxt.setText(f"{yields:.2f}%")

        except ValueError:
            # Manejar errores en caso de que el texto no sea un número válido
            self.yieldtxt.setText("Error: Introduce valores numéricos")

    def register(self):
        types = self.type_combobox.currentText()
        amount = self.amounttxt.text()
        amount_end = self.amount_endtxt.text()
        yields = self.yieldtxt.text()
        date = self.expiration_date.date().toString(
            "yyyy-MM-dd"
        )  # Obtiene la fecha del QDateEdit formateada

        if not type or not amount or not date:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.register(types, amount, amount_end, yields, date)
