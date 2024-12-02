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
from configuration.configuration_docx import report_doc
from configuration.configuration_size_window import set_default_size_and_center
from configuration.configuration_window_move import mousePressEvent, window_move
from controller.controllergoal import GoalController
from controller.controllerreport import ReportController


class Viewadd(QtWidgets.QMainWindow):
    def __init__(self, id_user):
        super(Viewadd, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainreportadd{self.theme}.ui", self)

        icon_configurate_top(self)
        set_default_size_and_center(self)
        delete_banner(self)

        # Establecer el código en el campo de texto codetxt
        self.usertxt.setText(f"{id_user}")

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

        self.controller = ReportController(self)

        self.btn_add.clicked.connect(self.register)

        self.cargar_datos_json_type_report()

    def cargar_datos_json_type_report(self):
        try:
            # Abre el archivo JSON
            with open("json/report_type.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("report_types", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                # Agregar los nombres de las regiones al QComboBox
                for types in names:
                    self.type_combobox.addItem(types["name"])

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

    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__()  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana

    def register(self):
        type_report = self.type_combobox.currentText()
        name = self.nametxt.text()
        file_name = f"{name}.docx"
        description = self.descriptiontxt.toPlainText()
        id_user = self.usertxt.text()

        if not type_report or not name or not description or not id_user:
            QMessageBox.warning(
                self, "Advertencia", "Todos los campos deben ser llenados."
            )
            return

        report_doc(id_user, name, type_report, description, file_name)

        # Registrar los datos en la base de datos (asumiendo que self.controller.register maneja esto)
        self.controller.register(id_user, name, type_report, description, file_name)
        QMessageBox.information(
            self, "Éxito", "El informe ha sido guardado y registrado correctamente."
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
