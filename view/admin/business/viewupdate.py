import json

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, Qt  # Qt se importa desde QtCore
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
from controller.controlleraddress import AddressController
from controller.controllerbusiness import BusinessController


class Viewupdate(QtWidgets.QMainWindow):

    def __init__(
        self,
        id,
        name,
        num_legal,
        industry,
        num_registro,
        date_founding,
        id_address,
        country,
        region,
        commune,
        address,
    ):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainbusinessupdate{self.theme}.ui", self)

        set_default_size_and_center(self)
        icon_configurate_top(self)
        delete_banner(self)

        self.uid = id
        self.id_address = id_address
        self.nametxt.setText(name)
        self.numlegaltxt.setText(num_legal)
        self.numregistertxt.setText(num_registro)
        self.datefoundingtxt.setDate(QDate.fromString(date_founding, "dd-MM-yyyy"))

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

        self.controller = BusinessController(self)
        self.controlleraddress = AddressController(self)

        self.btn_update.clicked.connect(self.update)
        self.btn_add_image.clicked.connect(self.add_image)

        self.cargar_datos_json_industry(industry)
        self.show_address(self.id_address, country, region, commune, address)

    def cargar_datos_json_industry(self, industry):
        try:
            # Abre el archivo JSON
            with open("json/industry.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("industries", [])

                self.industry_combobox.addItem(industry)

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                # Agregar los nombres de las regiones al QComboBox
                for industrys in names:
                    self.industry_combobox.addItem(industrys["name"])

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
        name = self.nametxt.text()
        num_legal = self.numlegaltxt.text()
        industry = self.industry_combobox.currentText()
        num_register = self.numregistertxt.text()
        date_founding = self.datefoundingtxt.text()
        address = self.address_combobox.currentData()
        image = self.imagetxt.text()

        if (
            not name
            or not num_legal
            or not industry
            or not num_register
            or not date_founding
        ):
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.update(
            self.uid,
            name,
            num_legal,
            industry,
            num_register,
            date_founding,
            address,
            image,
        )

    def show_address(self, id_address, country, region, commune, address):
        print(self.uid)
        # Desconectar la señal para evitar bucles infinitos
        self.address_combobox.blockSignals(True)

        # Concatenar country y region en una sola cadena
        address_str = f"{country} - {region} - {commune} - {address}"

        self.address_combobox.clear()

        # Añadir la concatenación de country y region al combobox
        self.address_combobox.addItem(address_str, id_address)
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
