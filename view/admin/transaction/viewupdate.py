import json

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt  # Qt se importa desde QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QSizeGrip
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


class Viewupdate(QtWidgets.QMainWindow):

    def __init__(self, uid, id_trans, date, amount, transaction_type, entity, payment):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/maintransactionupdate{self.theme}.ui", self)

        delete_banner(self)
        icon_configurate_top(self)
        set_default_size_and_center(self)

        self.uid = uid
        self.idtxt.setText(id_trans)
        self.datetxt.setText(date)
        self.amounttxt.setText(amount)

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

        self.controller = TransactionController(self)

        self.btn_update.clicked.connect(self.update)

        self.cargar_datos_json_type_transaction(transaction_type)
        self.cargar_datos_json_entity_transaction(entity)
        self.cargar_datos_json_type_payment_transaction(payment)

    def cargar_datos_json_type_transaction(self, transaction_type):
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

                self.transaction_type_combobox.addItem(transaction_type)

                # Agregar los nombres de las regiones al QComboBox
                for types in names:
                    self.transaction_type_combobox.addItem(types["name"])

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

    def cargar_datos_json_entity_transaction(self, entity):
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

                self.entity_combobox.addItem(entity)

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

    def cargar_datos_json_type_payment_transaction(self, payment):
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

                self.payment_combobox.addItem(payment)

                # Agregar los nombres de las regiones al QComboBox
                for types in names:
                    self.payment_combobox.addItem(types["name"])

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

    def update(self):
        date = self.datetxt.text()
        amount = self.amounttxt.text()
        type_transaction = self.transaction_type_combobox.currentText()
        entity = self.entity_combobox.currentText()
        type_payment = self.payment_combobox.currentText()

        if (
            not date
            or not amount
            or not type_transaction
            or not entity
            or not type_payment
        ):
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.update(
            self.uid, date, amount, type_transaction, entity, type_payment
        )

    def add_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Imagen",
            "",
            "Images (*.png *.xpm *.jpg);;All Files (*)",
            options=options,
        )
        if file_path:
            self.imagetxt.setText(file_path)  # Mostrar el path de la imagen (opcional)

            # Crear un QPixmap con la imagen seleccionada
            pixmap = QPixmap(file_path)

            # Ajustar el tamaño del QLabel y permitir que la imagen se escale
            self.image_label.setFixedSize(
                200, 200
            )  # Cambiar el tamaño del QLabel (ancho, alto)
            self.image_label.setScaledContents(
                True
            )  # La imagen se escala al tamaño del QLabel

            # Mostrar la imagen en el QLabel
            self.image_label.setPixmap(pixmap)

            # Centrar la imagen dentro del QLabel
            self.image_label.setAlignment(
                Qt.AlignCenter
            )  # Centrar horizontal y verticalmente
