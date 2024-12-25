import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox
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
from controller.controlleruser import UserController
from view.standar.address.viewmain import Viewmainaddress
from view.standar.business.viewmain import Viewmainbusiness
from view.standar.calendar.viewmain import Viewmaincalendar
from view.standar.client.viewmain import Viewmainclient
from view.standar.employee.viewmain import Viewmainemployee
from view.standar.gain.viewmain import Viewmaingain
from view.standar.goal.viewmain import Viewmaingoals
from view.standar.graphic.viewexpenses import ExpensesChart
from view.standar.graphic.viewgain import GainChart
from view.standar.graphic.viewinvestment import InvestmentChart
from view.standar.graphic.viewsale import SaleChart
from view.standar.graphic.viewtransaction import TransactionChart
from view.standar.inventory.viewmain import Viewmaininventory
from view.standar.investment.viewmain import Viewmaininvestment
from view.standar.invoice.viewmain import Viewmaininvoice
from view.standar.maps.viewmaps import MapaApp
from view.standar.print_sale.viewmain import PDFViewer
from view.standar.project.viewmain import Viewmainproject
from view.standar.provider.viewmain import Viewmainprovider
from view.standar.report.viewmain import Viewmainreport
from view.standar.sent.viewmain import Viewmainsent
from view.standar.task.viewmain import Viewmaintask
from view.standar.transaction.viewmain import Viewmaintransaction
from view.standar.user.profile.viewmain import Viewmainuserprofile
from view.standar.user.viewmain import Viewmainuser


class Viewdashboardstandar(QtWidgets.QMainWindow):
    def __init__(self, id_user, username):
        super(Viewdashboardstandar, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/standar/dashboard_standar{self.theme}.ui", self)

        self.id_user = id_user
        self.user_name = username

        self.btn_profile.setIcon(QIcon("img/user-profile.svg"))

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
        self.btn_invoice.clicked.connect(self.invoice)
        self.btn_client.clicked.connect(self.client)
        self.g_income.clicked.connect(self.graphic_income)
        self.g_expenses.clicked.connect(self.graphic_expenses)
        self.btn_pdf.clicked.connect(self.print_pdf)
        self.btn_provider.clicked.connect(self.provider)
        self.g_transaction.clicked.connect(self.graphic_transaction)
        self.btn_transaction.clicked.connect(self.transaction)
        self.btn_project.clicked.connect(self.project)
        self.btn_sent.clicked.connect(self.sent)
        self.g_investement.clicked.connect(self.graphic_investement)
        self.btn_investement.clicked.connect(self.investement)
        self.btn_task.clicked.connect(self.task)
        self.btn_business.clicked.connect(self.business)
        self.btn_gain.clicked.connect(self.gain)
        self.btn_calculate_gain.clicked.connect(self.graphic_gain)
        self.btn_goal.clicked.connect(self.goal)
        self.btn_report.clicked.connect(self.report)
        self.btn_calendar.clicked.connect(self.calendar)
        self.btn_employee.clicked.connect(self.employee)
        self.btn_address.clicked.connect(self.address)
        self.btn_maps.clicked.connect(self.maps)
        self.btn_profile.clicked.connect(self.profile)

        self.controlleruser = UserController(self)
        self.get_image_profile()

    def get_image_profile(self):
        # Llama al controlador para obtener los datos del usuario por ID
        user_data = self.controlleruser.get_image_profile(self.id_user)

        if user_data:
            # Asumiendo que el resultado es una tupla (id, nombre, correo, imagen_binaria, ...)
            user_image = user_data[0]  # Suponiendo que la imagen está en el índice 3

            if user_image:
                # Convertir los datos binarios de la imagen en un QPixmap
                pixmap = QPixmap()
                if pixmap.loadFromData(user_image):
                    # Redimensionar la imagen al tamaño deseado
                    size = 30  # Tamaño deseado
                    scaled_pixmap = pixmap.scaled(
                        size,
                        size,
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation,
                    )

                    # Crear un ícono a partir del pixmap
                    icon = QIcon(scaled_pixmap)
                    self.imagelabelprofile.setIcon(
                        icon
                    )  # Asigna el ícono al QPushButton
                    self.imagelabelprofile.setIconSize(
                        QSize(size, size)
                    )  # Ajusta el tamaño del ícono
                    self.imagelabelprofile.setIconSize(
                        QSize(size, size)
                    )  # Ajusta el tamaño del ícono
                    self.imagelabelprofile.setIconSize(
                        QSize(size, size)
                    )  # Ajusta el tamaño del ícono

                    # Carga la imagen desde los datos binarios

                else:
                    QMessageBox.warning(self, "Error", "No se pudo cargar la imagen")
            else:
                QMessageBox.warning(
                    self, "Error", "El usuario no tiene una imagen de perfil"
                )
        else:
            QMessageBox.warning(self, "Error", "Usuario no encontrado")

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

    def invoice(self):
        self.invoice_view = Viewmaininvoice(self.id_user, self.user_name)
        self.invoice_view.show()

    def client(self):
        self.client_view = Viewmainclient()
        self.client_view.show()

    def graphic_income(self):
        self.graphic_income_view = SaleChart()
        self.graphic_income_view.show()

    def graphic_expenses(self):
        self.graphic_expenses_view = ExpensesChart()
        self.graphic_expenses_view.show()

    def graphic_transaction(self):
        self.graphic_transaction_view = TransactionChart()
        self.graphic_transaction_view.show()

    def print_pdf(self):
        self.pdf_view = PDFViewer()
        self.pdf_view.show()

    def provider(self):
        self.provider_view = Viewmainprovider()
        self.provider_view.show()

    def transaction(self):
        self.trans_view = Viewmaintransaction()
        self.trans_view.show()

    def project(self):
        self.project_view = Viewmainproject()
        self.project_view.show()

    def sent(self):
        self.sent_view = Viewmainsent()
        self.sent_view.show()

    def investement(self):
        self.inv_view = Viewmaininvestment()
        self.inv_view.show()

    def task(self):
        self.task_view = Viewmaintask()
        self.task_view.show()

    def business(self):
        self.business_view = Viewmainbusiness()
        self.business_view.show()

    def gain(self):
        self.gain_view = Viewmaingain()
        self.gain_view.show()

    def graphic_gain(self):
        self.graphic_view_gain = GainChart()
        self.graphic_view_gain.show()

    def goal(self):
        self.view_goal = Viewmaingoals()
        self.view_goal.show()

    def report(self):
        self.view_report = Viewmainreport()
        self.view_report.show()

    def calendar(self):
        self.view_calendar = Viewmaincalendar()
        self.view_calendar.show()

    def employee(self):
        self.view_employee = Viewmainemployee()
        self.view_employee.show()

    def address(self):
        self.view_address = Viewmainaddress()
        self.view_address.show()

    def profile(self):
        self.view_profile = Viewmainuserprofile(self.id_user)
        self.view_profile.show()

    def maps(self):

        #   santiago de chile
        self.lat = -30.0000000
        self.lon = -71.0000000
        self.view_maps = MapaApp(self.lat, self.lon)
        self.view_maps.show()

    def graphic_investement(self):
        self.graphic_invest_view = InvestmentChart()
        self.graphic_invest_view.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = Viewdashboardstandar()
    mi_app.show()
    sys.exit(app.exec_())
