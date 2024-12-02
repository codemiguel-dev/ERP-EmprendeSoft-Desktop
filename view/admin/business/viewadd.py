import json

from PyQt5 import QtWidgets  # type: ignore
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
from controller.controlleraddress import AddressController
from controller.controllerbusiness import BusinessController
from controller.controlleruser import UserController
from view.admin.address.viewmain import Viewmainaddress


class Viewadd(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewadd, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainbusinessadd{self.theme}.ui", self)
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

        self.bt_minimizar.clicked.connect(lambda: control_bt_minimizar(self))
        self.bt_restaurar.clicked.connect(lambda: control_bt_normal(self))
        self.bt_maximizar.clicked.connect(lambda: control_bt_maximizar(self))
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_restaurar.hide()

        self.controller = BusinessController(self)
        self.controlleruser = UserController(self)
        self.controlleraddress = AddressController(self)

        # self.show_user()

        self.btn_add.clicked.connect(self.register)
        self.btn_address.clicked.connect(self.address)
        self.btn_add_image.clicked.connect(self.add_image)

        self.show_address()

        self.cargar_datos_json_industry()

    def cargar_datos_json_industry(self):
        try:
            # Abre el archivo JSON
            with open("json/industry.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("industries", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                # Agregar los nombres de las regiones al QComboBox
                for industry in names:
                    self.industry_combobox.addItem(industry["name"])

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
        address_id = self.address_combobox.currentData()
        name = self.nametxt.text()
        image = self.imagetxt.text()
        legal_form = self.legal_formtxt.text()
        industry = self.industry_combobox.currentText()
        registration_number = self.registration_numbertxt.text()
        founding_date = self.founding_datetxt.date().toString("yyyy-MM-dd")

        if not address_id or not name or not industry or not founding_date:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.register(
            address_id,
            name,
            image,
            legal_form,
            industry,
            registration_number,
            founding_date,
        )

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

    def address(self):
        self.view_address = Viewmainaddress()
        self.view_address.show()

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
