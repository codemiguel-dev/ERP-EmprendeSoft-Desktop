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
from controller.controllerinventory import InventoryController


class Viewupdate(QtWidgets.QMainWindow):
    def __init__(
        self, uid, name, category, stock, pricepurch, pricesale, totalpurch, description
    ):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/maininventoryupdate{self.theme}.ui", self)

        set_default_size_and_center(self)
        icon_configurate_top(self)
        delete_banner(self)

        self.sale_total = 0.0

        self.uid = uid
        self.nametxt.setText(name)
        self.descriptiontxt.setText(description)
        self.categorytxt.setText(category)
        self.stocktxt.setText(stock)
        self.pricepurchtxt.setText(pricepurch)
        self.pricesaletxt.setText(pricesale)
        self.totaltxt.setText(totalpurch)

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

        self.controller = InventoryController(self)

        self.btn_update.clicked.connect(self.update_inventory)
        self.btn_calculate_total.clicked.connect(self.calculate_total)
        self.btn_add_image.clicked.connect(self.add_image)

    def clear_fields(self):
        """Limpia todos los campos de entrada."""
        self.nametxt.clear()
        self.categorytxt.clear()
        self.stocktxt.clear()
        self.pricepurchtxt.clear()
        self.pricesaletxt.clear()

    def calculate_total(self):
        stock = self.stocktxt.text()
        pricepurch = self.pricepurchtxt.text()

        try:
            # Convertir las cadenas a números
            priceproduct = float(pricepurch)
            stockproduct = int(stock)

            # Calcular el total de cada producto
            self.total = priceproduct * stockproduct

            # Sumar el total del producto al total acumulado
            # self.sale_total += total

            self.totaltxt.setText(f"{self.total}")

        except ValueError:
            # Manejar el caso en el que la conversión falla
            self.labeltotal.setText("Error: Valores inválidos")

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

    def update_inventory(self):
        name = self.nametxt.text()
        category = self.categorytxt.text()
        stock = self.stocktxt.text()
        purchase_price = self.pricepurchtxt.text()
        sale_price = self.pricesaletxt.text()
        totalpurch = self.totaltxt.text()
        description = self.descriptiontxt.toPlainText()
        image = self.imagetxt.text()

        if (
            not name
            or not category
            or not stock
            or not purchase_price
            or not sale_price
            or not description
            or not totalpurch
        ):
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.update_inventory(
            self.uid,
            name,
            category,
            stock,
            purchase_price,
            sale_price,
            totalpurch,
            description,
            image,
        )
