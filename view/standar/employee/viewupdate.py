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


class Viewupdate(QtWidgets.QMainWindow):

    def __init__(self, uid, name_user, id_employee, job):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainemployeupdate{self.theme}.ui", self)

        set_default_size_and_center(self)
        icon_configurate_top(self)
        delete_banner(self)

        self.uid = uid
        self.id_employee = id_employee

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

        self.btn_update.clicked.connect(self.update)

        self.show_user(name_user, uid)
        self.get_json_job(job)

    def update(self):
        user_id = self.user_combobox.currentData()
        job = self.job_combobox.currentText()

        if not user_id or not job:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.update(self.uid, user_id, self.id_employee, job)

    def show_user(self, name_user, uid):
        # Desconectar la señal para evitar bucles infinitos
        self.user_combobox.blockSignals(True)

        self.user_combobox.clear()

        self.user_combobox.addItem(name_user, uid)
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

    def get_json_job(self, job):
        try:
            # Abre el archivo JSON
            with open("json/job.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                jobs = self.datos.get("job", [])

                if not jobs:
                    raise ValueError("No se encontraron datos en 'shipping_methods'")

                # imprimir status en combobox
                self.job_combobox.addItem(job)

                # Agregar los nombres de las regiones al QComboBox
                for status_task in jobs:
                    self.job_combobox.addItem(status_task["name"])

                # Conectar la señal de cambio de región
                # self.region_combobox.currentIndexChanged.connect(self.cargar_datos_json_commune)

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Archivo JSON no encontrado.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(
                self, "Error de JSON", f"Error al decodificar el archivo JSON: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {str(e)}")
