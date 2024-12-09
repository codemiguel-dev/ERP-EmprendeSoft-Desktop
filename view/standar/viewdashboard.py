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
from view.standar.client.viewmain import Viewmainclient
from view.standar.graphic.viewexpenses import ExpensesChart
from view.standar.graphic.viewinvestment import InvestmentChart
from view.standar.graphic.viewsale import SaleChart
from view.standar.graphic.viewtransaction import TransactionChart
from view.standar.inventory.viewmain import Viewmaininventory
from view.standar.invoice.viewmain import Viewmaininvoice
from view.standar.print_sale.viewmain import PDFViewer
from view.standar.project.viewmain import Viewmainproject
from view.standar.provider.viewmain import Viewmainprovider
from view.standar.sent.viewmain import Viewmainsent
from view.standar.transaction.viewmain import Viewmaintransaction
from view.standar.user.viewmain import Viewmainuser


class Viewdashboardstandar(QtWidgets.QMainWindow):
    def __init__(self, id_user, username):
        super(Viewdashboardstandar, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/standar/dashboard_standar{self.theme}.ui", self)

        self.id_user = id_user
        self.user_name = username

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

    def graphic_investement(self):
        self.graphic_invest_view = InvestmentChart()
        self.graphic_investement_view.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = Viewdashboardstandar()
    mi_app.show()
    sys.exit(app.exec_())
