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
from controller.controlleremployee import EmployeeController
from controller.controlleruser import UserController


class Viewadd(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewadd, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainemployeeadd{self.theme}.ui", self)

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

        self.controller = EmployeeController(self)
        self.controlleruser = UserController(self)

        # self.show_user()

        self.btn_add.clicked.connect(self.register)
        # self.btn_address.clicked.connect(self.address)

        self.show_user()
        self.json_job()

    def json_job(self):
        try:
            # Abre el archivo JSON
            with open("json/job.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("job", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                # Agregar los nombres de las regiones al QComboBox
                for types in names:
                    self.job_combobox.addItem(types["name"])

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

    def show_user(self):
        # Desconectar la señal para evitar bucles infinitos
        self.comboboxuser.blockSignals(True)

        self.comboboxuser.clear()
        # Obtener datos de inventario desde el controlador
        users = self.controlleruser.get_user()

        # Añadir productos al comboBox
        for client in users:
            uid = client[0]  # El primer elemento es el ID del producto
            name = client[2]  # El segundo elemento es el nombre del producto

            # Añadir el producto al combobox
            self.comboboxuser.addItem(name, uid)

        # Reconectar la señal después de añadir los productos
        self.comboboxuser.blockSignals(False)

    def register(self):
        user_id = self.comboboxuser.currentData()
        job = self.job_combobox.currentText()

        if not user_id or not job:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.register(user_id, job)
