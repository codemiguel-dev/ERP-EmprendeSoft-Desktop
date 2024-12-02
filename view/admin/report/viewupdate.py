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
from controller.controllertask import TaskController
from controller.controlleruser import UserController


class Viewupdate(QtWidgets.QMainWindow):
    def __init__(self, uid, id_task, user, name, description, status):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainreportupdate{self.theme}.ui", self)

        set_default_size_and_center(self)
        delete_banner(self)
        icon_configurate_top(self)

        self.sale_total = 0.0

        self.id_task = id_task
        self.nametxt.setText(name)
        self.descriptiontxt.setText(description)

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

        self.controller = TaskController(self)
        self.controlleruser = UserController(self)

        self.btn_update.clicked.connect(self.update)

        self.show_user(user, uid)
        self.get_json_status(status)

    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__()  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana

    def update(self):
        user_id = self.user_combobox.currentData()  # obtiene id
        name = self.nametxt.text()
        description = self.descriptiontxt.toPlainText()
        status = self.status_combobox.currentText()

        if not name or not description or not status:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.update(self.id_task, user_id, name, description, status)

    def show_user(self, user, uid):
        # Desconectar la señal para evitar bucles infinitos
        self.user_combobox.blockSignals(True)

        self.user_combobox.clear()

        self.user_combobox.addItem(user, uid)
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

    def get_json_status(self, status_ta):
        try:
            # Abre el archivo JSON
            with open("json/status_task.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                status = self.datos.get("status", [])

                if not status:
                    raise ValueError("No se encontraron datos en 'shipping_methods'")

                # imprimir status en combobox
                self.status_combobox.addItem(status_ta)

                # Agregar los nombres de las regiones al QComboBox
                for status_task in status:
                    self.status_combobox.addItem(status_task["name"])

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
