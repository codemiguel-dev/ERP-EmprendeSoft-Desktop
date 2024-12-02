from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate  # Qt se importa desde QtCore
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
from controller.controllerinvestment import InvestmentController


class Viewupdate(QtWidgets.QMainWindow):
    def __init__(self, uid, types, date, amount, amount_end, yields, expiration_date):
        super(Viewupdate, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/maininvestmentupdate{self.theme}.ui", self)

        set_default_size_and_center(self)
        icon_configurate_top(self)
        delete_banner(self)

        expiration_date_obj = QDate.fromString(expiration_date, "yyyy-MM-dd")

        self.sale_total = 0.0

        self.uid = uid
        self.type_combobox.setCurrentText(types)
        self.datetxt.setText(date)
        self.amounttxt.setText(amount)
        self.amount_endtxt.setText(amount_end)
        self.yieldtxt.setText(yields)
        self.expiration_date.setDate(expiration_date_obj)

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

        self.controller = InvestmentController(self)

        self.btn_update.clicked.connect(self.update)
        self.btn_calculate_yield.clicked.connect(self.calculate_yield)

    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__()  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana

    def clear_fields(self):
        """Limpia todos los campos de entrada."""
        self.nametxt.clear()
        self.categorytxt.clear()
        self.stocktxt.clear()
        self.pricepurchtxt.clear()
        self.pricesaletxt.clear()

    def calculate_yield(self):
        try:
            # Obtener los valores desde los campos de texto
            amount = float(self.amounttxt.text())  # Valor inicial
            amount_end = float(self.amount_endtxt.text())  # Valor final

            # Calcular el rendimiento
            yields = ((amount_end - amount) / amount) * 100

            # Mostrar el rendimiento calculado en el campo de texto yieldtxt
            self.yieldtxt.setText(f"{yields:.2f}%")

        except ValueError:
            # Manejar errores en caso de que el texto no sea un número válido
            self.yieldtxt.setText("Error: Introduce valores numéricos")

    def update(self):
        types = self.type_combobox.currentText()
        amount = self.amounttxt.text()
        amount_end = self.amount_endtxt.text()
        yields = self.yieldtxt.text()
        date_expiration = self.expiration_date.date().toString("yyyy-MM-dd")

        if (
            not type
            or not amount
            or not amount_end
            or not yields
            or not date_expiration
        ):
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.update(
            self.uid, types, amount, amount_end, yields, date_expiration
        )
