import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

from configuration.configuration_buttom import icon_configurate_exit_session
from configuration.configuration_buttom_top import (
    control_bt_maximizar,
    control_bt_minimizar,
    control_bt_normal,
)
from configuration.configuration_config_theme import load_config
from configuration.configuration_dash_icon import icons_dash_buttom
from configuration.configuration_delete_banner import delete_banner
from configuration.configuration_window_move import mousePressEvent, window_move
from view.standar.inventory.viewmain import Viewmaininventory
from view.standar.user.viewmain import Viewmainuser


class Viewdashboardstandar(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewdashboardstandar, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/standar/dashboard_standar{self.theme}.ui", self)

        icon_configurate_exit_session(self)
        icons_dash_buttom(self)
        delete_banner(self)

        # Configurar SizeGrip para redimensionar la ventana
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

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

        self.btn_inventory.clicked.connect(self.inventory)
        self.btn_user.clicked.connect(self.user)
        self.bt_exit_session.clicked.connect(self.exit_session)

    def exit_session(self):
        self.close()
        from view.viewlogin import LoginView

        self.view_login = LoginView()
        self.view_login.show()

    def inventory(self):
        self.inventory_view = Viewmaininventory()
        self.inventory_view.show()

    def user(self):
        self.user_view = Viewmainuser()
        self.user_view.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = Viewdashboardstandar()
    mi_app.show()
    sys.exit(app.exec_())
