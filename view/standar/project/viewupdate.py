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
from controller.controllerproject import ProjectController


class Viewupdate(QtWidgets.QMainWindow):
    def __init__(self, uid, name, description, budget, status, type_project):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/mainprojectupdate{self.theme}.ui", self)

        set_default_size_and_center(self)
        icon_configurate_top(self)
        delete_banner(self)

        self.sale_total = 0.0

        self.uid = uid
        self.nametxt.setText(name)
        self.descriptiontxt.setText(description)
        self.budgettxt.setText(budget)

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

        self.controller = ProjectController(self)

        self.btn_update.clicked.connect(self.update)

        # get json
        self.cargar_datos_json_type_project(type_project)
        self.cargar_datos_json_status_project(status)

    def cargar_datos_json_status_project(self, status):
        try:
            # Abre el archivo JSON
            with open(
                "json/status_project.json", "r", encoding="utf-8"
            ) as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("status", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                self.status_combobox.addItem(status)
                # Agregar los nombres de las regiones al QComboBox
                for status in names:
                    self.status_combobox.addItem(status["name"])

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

    def cargar_datos_json_type_project(self, type_project):
        try:
            # Abre el archivo JSON
            with open("json/type_project.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("type_project", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                self.type_combobox.addItem(type_project)

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

    def update(self):
        name = self.nametxt.text()
        description = self.descriptiontxt.toPlainText()
        budget = self.budgettxt.text()
        status = self.status_combobox.currentText()
        type_project = self.type_combobox.currentText()

        if not name or not description or not budget or not status or not type_project:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.update(
            self.uid, name, description, budget, status, type_project
        )
