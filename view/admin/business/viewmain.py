from PyQt5 import QtWidgets
from PyQt5.Qt import QIODevice
from PyQt5.QtCore import QBuffer, QByteArray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox, QSizeGrip
from PyQt5.uic import loadUi

from configuration.configuration_buttom import (
    icon_configurate_manager,
    icon_configurate_top,
    icon_exit_program,
)
from configuration.configuration_buttom_top import (
    control_bt_maximizar,
    control_bt_minimizar,
    control_bt_normal,
)
from configuration.configuration_config_theme import load_config
from configuration.configuration_delete_banner import delete_banner
from configuration.configuration_window_move import mousePressEvent, window_move
from controller.controlleraddress import AddressController
from controller.controllerbusiness import BusinessController
from view.admin.business.viewadd import Viewadd
from view.admin.business.viewupdate import Viewupdate


class Viewmainbusiness(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewmainbusiness, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainbusiness{self.theme}.ui", self)

        icon_configurate_manager(self)
        icon_configurate_top(self)
        icon_exit_program(self)
        delete_banner(self)

        # Inicializar el QSizeGrip y establecer su tamaño
        self.gripSize = 16  # Define el tamaño del grip
        self.grip = QSizeGrip(self)  # Crea un QSizeGrip para el redimensionamiento
        self.grip.resize(self.gripSize, self.gripSize)  # Ajusta el tamaño del QSizeGrip

        # Maximizar la ventana por defecto
        self.showMaximized()

        # Asigna los eventos personalizados al frame superior
        self.frame_superior.mousePressEvent = lambda event: mousePressEvent(self, event)
        self.frame_superior.mouseMoveEvent = lambda event: window_move(self, event)

        # Control de botones de la barra de títulos
        self.bt_minimizar.clicked.connect(lambda: control_bt_minimizar(self))
        self.bt_restaurar.clicked.connect(lambda: control_bt_normal(self))
        self.bt_maximizar.clicked.connect(lambda: control_bt_maximizar(self))
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_maximizar.hide()

        self.btn_add.clicked.connect(self.add)
        self.btn_get.clicked.connect(self.show)
        self.btn_update.clicked.connect(self.update)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_exit.clicked.connect(self.close_program)

        self.controller = BusinessController(self)

        self.controlleraddress = AddressController(self)

        self.show()

    def close_program(self):
        QApplication.quit()

    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__()  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana

    def add(self):
        self.business_add = Viewadd()
        self.business_add.show()

    def show(self):
        # Obtener datos desde el controlador (usando el INNER JOIN)
        Business_controller = self.controller.get()

        for i, business in enumerate(Business_controller):
            if isinstance(business, (tuple, list)):
                # Asignar los datos a los QLabel correspondientes
                self.label_id.setText(f"ID: {business[0]}")
                self.label_name.setText(f"Nombre: {business[1]}")

                # Mostrar la imagen almacenada como BLOB en el QLabel
                image_blob = business[
                    2
                ]  # Asumiendo que `business[2]` contiene el BLOB de la imagen
                if image_blob:
                    pixmap = self.convert_blob_to_pixmap(image_blob)
                    if not pixmap.isNull():
                        self.label_image.setPixmap(pixmap)
                        self.label_image.setScaledContents(
                            True
                        )  # Ajusta la imagen al tamaño del QLabel
                    else:
                        self.label_image.setText("Imagen no encontrada")
                else:
                    self.label_image.setText("Sin imagen disponible")

                self.label_legal_form.setText(f"N. Legal: {business[3]}")
                self.label_industry.setText(f"Industria: {business[4]}")
                self.label_registration_number.setText(
                    f"Número de Registro: {business[5]}"
                )
                self.label_founding_date.setText(f"Fecha de Fundación: {business[6]}")
                self.id_address = business[7]
                self.label_country.setText(f"Pais: {business[8]}")
                self.label_region.setText(f"Region: {business[9]}")
                self.label_commune.setText(f"Comuna: {business[10]}")
                self.label_description.setText(f"Dirección: {business[11]}")

                break  # Mostrar un solo registro

        # Función auxiliar para convertir BLOB a QPixmap

    def convert_blob_to_pixmap(self, blob_data):
        """Convierte un BLOB de imagen a un QPixmap"""
        byte_array = QByteArray(blob_data)
        pixmap = QPixmap()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.ReadOnly)
        pixmap.loadFromData(buffer.data())
        return pixmap

    def update(self):
        # Obtener datos desde el controlador (usando el INNER JOIN)
        Business_controller = self.controller.get()

        for i, business in enumerate(Business_controller):
            if isinstance(business, (tuple, list)):
                # Asignar los datos a los QLabel correspondientes
                self.id = business[0]
                self.name = business[1]
                self.image = business[2]
                self.num_legal = business[3]
                self.industry = business[4]
                self.num_registro = business[5]
                self.date_founding = business[6]
                self.id_address = business[7]
                self.country = business[8]
                self.region = business[9]
                self.commune = business[10]
                self.address = business[11]

                break  # Mostrar un solo registro

        # Abrir el nuevo formulario de actualización
        self.update_form = Viewupdate(
            self.id,
            self.name,
            self.num_legal,
            self.industry,
            self.num_registro,
            self.date_founding,
            self.id_address,
            self.country,
            self.region,
            self.commune,
            self.address,
        )
        self.update_form.show()

    def delete(self):
        Business_controller = self.controller.get()
        for i, business in enumerate(Business_controller):
            if isinstance(business, (tuple, list)):
                # Asignar los datos a los QLabel correspondientes
                self.id = business[0]
                break  # Mostrar un solo registro

        uid = self.id
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que deseas eliminar este registro?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.controller.delete(uid)
            QMessageBox.information(
                self, "Información", "Registro eliminado correctamente."
            )
            self.show()
        else:
            QMessageBox.information(
                self, "Información", "Operación de eliminación cancelada."
            )

    def search(self):
        search_text = self.searchtxt.text().lower()  # Texto de búsqueda en minúsculas
        found = False  # Variable para rastrear si se encontró una coincidencia

        for row in range(self.table_client.rowCount()):
            match = False
            for col in range(self.table_client.columnCount()):
                item = self.table_client.item(row, col)
                if item and search_text in item.text().lower():  # Comparar texto
                    match = True
                    found = True  # Si hay una coincidencia, actualizamos 'found'
                    break  # Si encuentra coincidencia, no sigue buscando en esa fila

            # Ocultar la fila si no coincide
            self.table_client.setRowHidden(row, not match)

        # Si no se encontró ninguna coincidencia, mostrar un mensaje de advertencia
        if not found:
            QtWidgets.QMessageBox.warning(
                self,
                "Sin coincidencias",
                "No se encontraron resultados para la búsqueda.",
            )
