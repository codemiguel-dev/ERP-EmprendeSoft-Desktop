import json
import uuid

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
from controller.controllertransaction import TransactionController


class Viewadd(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewadd, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/maintransactionadd{self.theme}.ui", self)

        delete_banner(self)
        set_default_size_and_center(self)
        icon_configurate_top(self)

        # Inicializar el QSizeGrip y establecer su tamaño
        self.gripSize = 16  # Define el tamaño del grip
        self.grip = QSizeGrip(self)  # Crea un QSizeGrip para el redimensionamiento
        self.grip.resize(self.gripSize, self.gripSize)  # Ajusta el tamaño del QSizeGrip

        # Asigna los eventos personalizados al frame superior
        self.frame_superior.mousePressEvent = lambda event: mousePressEvent(self, event)
        self.frame_superior.mouseMoveEvent = lambda event: window_move(self, event)

        amount = 000.0
        self.amounttxt.setText(str(amount))

        # Control de botones de la barra de títulos
        self.bt_minimizar.clicked.connect(lambda: control_bt_minimizar(self))
        self.bt_restaurar.clicked.connect(lambda: control_bt_normal(self))
        self.bt_maximizar.clicked.connect(lambda: control_bt_maximizar(self))
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_restaurar.hide()

        self.controller = TransactionController(self)

        self.btn_add.clicked.connect(self.register)
        self.btn_generate.clicked.connect(self.generate_id)

        self.cargar_datos_json_type_transaction()
        self.cargar_datos_json_entity_transaction()
        self.cargar_datos_json_type_payment_transaction()

    def cargar_datos_json_type_transaction(self):
        try:
            # Abre el archivo JSON
            with open(
                "json/transaction_type.json", "r", encoding="utf-8"
            ) as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("transaction_type", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                # Agregar los nombres de las regiones al QComboBox
                for types in names:
                    self.type_trans_combobox.addItem(types["name"])

                # Conectar la señal de cambio de región
                # self.industry_combobox.currentIndexChanged.connect(self.cargar_datos_json_commune)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Archivo JSON no encontrado.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(
                self, "Error de JSON", f"Error al decodificar el archivo JSON: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {str(e)}")

    def cargar_datos_json_entity_transaction(self):
        try:
            # Abre el archivo JSON
            with open(
                "json/transaction_entity.json", "r", encoding="utf-8"
            ) as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("transaction_entity", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                # Agregar los nombres de las regiones al QComboBox
                for types in names:
                    self.entity_combobox.addItem(types["name"])

                # Conectar la señal de cambio de región
                # self.industry_combobox.currentIndexChanged.connect(self.cargar_datos_json_commune)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Archivo JSON no encontrado.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(
                self, "Error de JSON", f"Error al decodificar el archivo JSON: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {str(e)}")

    def cargar_datos_json_type_payment_transaction(self):
        try:
            # Abre el archivo JSON
            with open(
                "json/transaction_type_payment.json", "r", encoding="utf-8"
            ) as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("transaction_type_payment", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                # Agregar los nombres de las regiones al QComboBox
                for types in names:
                    self.type_pay_combobox.addItem(types["name"])

                # Conectar la señal de cambio de región
                # self.industry_combobox.currentIndexChanged.connect(self.cargar_datos_json_commune)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Archivo JSON no encontrado.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(
                self, "Error de JSON", f"Error al decodificar el archivo JSON: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {str(e)}")

    def register(self):
        id_trans = self.idtxt.text()
        amount = self.amounttxt.text()
        type_trans = self.type_trans_combobox.currentText()
        entity = self.entity_combobox.currentText()
        type_pay = self.type_pay_combobox.currentText()

        if not id_trans or not amount or not type_trans or not entity or not type_pay:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.register(id_trans, amount, type_trans, entity, type_pay)

    def generate_id(self):
        # Generar código único
        code = f"TRANS-{uuid.uuid4().hex[:8].upper()}"

        # Establecer el código en el campo de texto codetxt
        self.idtxt.setText(code)
