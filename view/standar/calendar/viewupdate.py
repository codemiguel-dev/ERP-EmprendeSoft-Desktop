from PyQt5 import QtCore, QtWidgets
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
from controller.controllercalendar import CalendarController
from controller.controlleremployee import EmployeeController


class Viewupdate(QtWidgets.QMainWindow):

    def __init__(self, id_horary, name_employee, start_time, end_time, horary):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/maincalendarupdate{self.theme}.ui", self)

        set_default_size_and_center(self)
        icon_configurate_top(self)
        delete_banner(self)

        self.uid = id_horary
        self.employee_combobox.addItem(name_employee)
        self.start_time_timeedit.setTime(QtCore.QTime.fromString(start_time, "HH:mm"))
        self.end_time_timeedit.setTime(QtCore.QTime.fromString(end_time, "HH:mm"))
        self.horarytxt.setText(horary)

        # Eliminar barra de título y hacer la ventana translúcida
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

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

        self.controller = CalendarController(self)
        self.controlleremployee = EmployeeController(self)

        self.btn_update.clicked.connect(self.update)
        self.show_employee()

    def show_employee(self):
        # Desconectar la señal para evitar bucles infinitos
        self.employee_combobox.blockSignals(True)

        self.employee_combobox.clear()
        # Obtener datos de inventario desde el controlador
        employes = self.controlleremployee.get()

        # Añadir productos al comboBox
        for employee in employes:
            uid = employee[2]  # El primer elemento es el ID del producto
            name = employee[1]  # El segundo elemento es el nombre del producto

            # Añadir el producto al combobox
            self.employee_combobox.addItem(name, uid)

        # Reconectar la señal después de añadir los productos
        self.employee_combobox.blockSignals(False)

    def update(self):
        employee = self.employee_combobox.currentData()
        start_time = self.start_time_timeedit.time().toString(
            "HH:mm"
        )  # Corregido a 'timeedit'
        end_time = self.end_time_timeedit.time().toString(
            "HH:mm"
        )  # Corregido a 'timeedit'
        horary = self.horarytxt.text()

        if not employee or not start_time or not end_time or not horary:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.update(self.uid, employee, start_time, end_time, horary)
