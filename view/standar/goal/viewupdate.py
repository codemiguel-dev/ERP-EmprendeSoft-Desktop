import json

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
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
from controller.controllergoal import GoalController


class Viewupdate(QtWidgets.QMainWindow):

    def __init__(
        self,
        uid_goal,
        name_goal,
        description_goal,
        status_goal,
        start_date,
        end_date,
        id_business,
        name_business,
    ):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/maingoalupdate{self.theme}.ui", self)

        set_default_size_and_center(self)
        icon_configurate_top(self)
        delete_banner(self)

        self.id_goal = uid_goal
        self.nametxt.setText(name_goal)
        self.descriptiontxt.setText(description_goal)

        self.id_business = id_business
        self.name_businesstxt.setText(name_business)

        # Establecer las fechas en los QCalendarWidgets
        self.start_datetxt.setSelectedDate(QDate.fromString(start_date, "yyyy-MM-dd"))
        self.end_datetxt.setSelectedDate(QDate.fromString(end_date, "yyyy-MM-dd"))

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

        self.controller = GoalController(self)

        self.btn_update.clicked.connect(self.update)

        self.cargar_datos_json_status(status_goal)

    def cargar_datos_json_status(self, status_goal):
        try:
            # Abre el archivo JSON
            with open("json/status_goal.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("status", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                self.status_combobox.addItem(status_goal)
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

    def update_start_date(self):
        self.start_date = self.start_datetxt.selectedDate().toString("yyyy-MM-dd")
        print(f"Fecha de inicio: {self.start_date}")

    def update_end_date(self):
        self.end_date = self.end_datetxt.selectedDate().toString("yyyy-MM-dd")
        print(f"Fecha de finalización: {self.end_date}")

    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__()  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana

    def update(self):
        name = self.nametxt.text()
        descripcion = self.descriptiontxt.toPlainText()

        if not name or not descripcion:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        # Obtener las fechas seleccionadas
        start_date = self.start_datetxt.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_datetxt.selectedDate().toString("yyyy-MM-dd")

        self.controller.update(self.id_goal, name, descripcion, start_date, end_date)
