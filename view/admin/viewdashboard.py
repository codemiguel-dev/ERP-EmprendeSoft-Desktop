import configparser
import json
import os
import sys

import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
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
from controller.controllerbusiness import BusinessController
from controller.controllerinventory import InventoryController
from controller.controllerinvestment import InvestmentController
from controller.controllerinvoice import InvoiceController
from controller.controllertask import TaskController
from controller.controllertransaction import TransactionController
from view.admin.address.viewmain import Viewmainaddress
from view.admin.business.viewmain import Viewmainbusiness
from view.admin.calendar.viewmain import Viewmaincalendar
from view.admin.client.viewmain import Viewmainclient
from view.admin.employee.viewmain import Viewmainemployee
from view.admin.gain.viewmain import Viewmaingain
from view.admin.goal.viewmain import Viewmaingoals
from view.admin.graphic.viewexpenses import ExpensesChart
from view.admin.graphic.viewgain import GainChart
from view.admin.graphic.viewinvestment import InvestmentChart
from view.admin.graphic.viewsale import SaleChart
from view.admin.graphic.viewtransaction import TransactionChart
from view.admin.inventory.viewmain import Viewmaininventory
from view.admin.investment.viewmain import Viewmaininvestment
from view.admin.invoice.viewmain import Viewmaininvoice
from view.admin.maps.viewmaps import MapaApp
from view.admin.print_sale.viewmain import PDFViewer
from view.admin.project.viewmain import Viewmainproject
from view.admin.provider.viewmain import Viewmainprovider
from view.admin.report.viewmain import Viewmainreport
from view.admin.sent.viewmain import Viewmainsent
from view.admin.task.viewmain import Viewmaintask
from view.admin.transaction.viewmain import Viewmaintransaction
from view.admin.user.viewmain import Viewmainuser

CONFIG_FILE = "positions.json"


class Viewdashboradadmin(QtWidgets.QMainWindow):
    def __init__(self, id_user):
        super(Viewdashboradadmin, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/admin/dashboardadmin{self.theme}.ui", self)

        self.label_id_session.setText(f"ID de Usuario: {id_user}")
        self.id_user = id_user

        self.bt_maximizar.hide()

        icon_configurate_exit_session(self)
        icons_dash_buttom(self)
        delete_banner(self)

        # Conectar el botón para cambiar el tema
        self.btn_theme0.clicked.connect(self.change_theme_to_theme)
        self.btn_theme1.clicked.connect(self.change_theme_to_theme1)
        self.btn_theme2.clicked.connect(self.change_theme_to_theme2)
        self.btn_theme3.clicked.connect(self.change_theme_to_theme3)
        self.btn_theme4.clicked.connect(self.change_theme_to_theme4)

        self.btn_inventory.clicked.connect(self.inventory)
        self.btn_user.clicked.connect(self.user)
        self.btn_client.clicked.connect(self.client)
        self.btn_provider.clicked.connect(self.provider)
        self.btn_pdf.clicked.connect(self.print_sale)
        self.g_income.clicked.connect(self.graphi_income)
        self.g_expenses.clicked.connect(self.graphi_expenses)
        self.btn_invoice.clicked.connect(self.invoice)
        self.btn_transaction.clicked.connect(self.transaction)
        self.g_transaction.clicked.connect(self.graphi_transaction)
        self.g_investement.clicked.connect(self.graphi_investment)
        self.btn_project.clicked.connect(self.project)
        self.btn_sent.clicked.connect(self.sent)
        self.btn_investement.clicked.connect(self.investment)
        self.btn_task.clicked.connect(self.task)
        self.btn_goal.clicked.connect(self.goal)
        self.btn_business.clicked.connect(self.business)
        self.btn_address.clicked.connect(self.address)
        self.btn_maps.clicked.connect(self.maps)
        self.btn_calculate_gain.clicked.connect(self.graphi_gain)
        self.btn_gain.clicked.connect(self.gain)
        self.btn_report.clicked.connect(self.report)
        self.btn_employee.clicked.connect(self.employee)
        self.btn_calendar.clicked.connect(self.calendar)
        self.bt_exit_session.clicked.connect(self.exit_session)

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

        self.controller = InventoryController(self)
        self.controllerinvestment = InvestmentController(self)
        self.controllerinvoice = InvoiceController(self)
        self.controllertransaction = TransactionController(self)
        self.controllerbusiness = BusinessController(self)

    def exit_session(self):
        self.close()
        from view.viewlogin import LoginView

        self.view_login = LoginView()
        self.view_login.show()

    def load_positions(self):
        """Cargar las posiciones de los botones desde el archivo JSON."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                positions = json.load(file)

                # Restaurar la posición de cada botón
                # self.button1.move(QPoint(*positions.get("button1", [50, 50])))
                # self.button2.move(QPoint(*positions.get("button2", [150, 50])))

        else:
            # Posiciones por defecto si no existe el archivo
            self.reset_positions()  # Restablecer si no hay datos guardados

    def save_positions(self):
        """Guardar las posiciones de los botones en el archivo JSON."""
        positions = {
            "btn_inventory": [
                self.btn_inventory.pos().x(),
                self.btn_inventory.pos().y(),
            ]
        }
        with open(CONFIG_FILE, "w") as file:
            json.dump(positions, file)

    def reset_positions(self):
        """Restablecer posiciones de los botones a sus valores por defecto."""
        # Mover los botones a las posiciones por defecto
        # self.button1.move(50, 50)
        # self.button2.move(150, 50)

        # Guardar las posiciones por defecto en el archivo JSON
        self.save_positions()

    def closeEvent(self, event):
        """Guardar posiciones cuando la ventana se cierra."""
        self.save_positions()
        event.accept()

    def save_config(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        if "Settings" not in config:
            config.add_section("Settings")

        config.set("Settings", "theme", self.theme)

        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def change_theme_to_theme(self):
        self.theme = "0"
        self.save_config()
        self.reload_ui()

    def change_theme_to_theme1(self):
        self.theme = "1"
        self.save_config()
        self.reload_ui()

    def change_theme_to_theme2(self):
        self.theme = "2"
        self.save_config()
        self.reload_ui()

    def change_theme_to_theme3(self):
        self.theme = "3"
        self.save_config()
        self.reload_ui()

    def change_theme_to_theme4(self):
        self.theme = "4"
        self.save_config()
        self.reload_ui()

    def inventory(self):
        self.inventory_view = Viewmaininventory()
        self.inventory_view.show()

    def user(self):
        self.user_view = Viewmainuser()
        self.user_view.show()

    def client(self):
        self.client_view = Viewmainclient()
        self.client_view.show()

    def provider(self):
        self.provider_view = Viewmainprovider()
        self.provider_view.show()

    def print_sale(self):
        self.sale_view = PDFViewer()
        self.sale_view.show()

    def invoice(self):
        self.invoice_view = Viewmaininvoice()
        self.invoice_view.show()

    def transaction(self):
        self.transaction_view = Viewmaintransaction()
        self.transaction_view.show()

    def project(self):
        self.project_view = Viewmainproject()
        self.project_view.show()

    def sent(self):
        self.sell_view = Viewmainsent()
        self.sell_view.show()

    def investment(self):
        self.investment_view = Viewmaininvestment()
        self.investment_view.show()

    def task(self):
        self.task_view = Viewmaintask()
        self.task_view.show()

    def goal(self):
        self.goal_view = Viewmaingoals()
        self.goal_view.show()

    def business(self):
        self.business_view = Viewmainbusiness()
        self.business_view.show()

    def address(self):
        self.address_view = Viewmainaddress()
        self.address_view.show()

    def maps(self):
        """Obtiene las coordenadas de latitud y longitud para una dirección dada y muestra el mapa."""
        # geolocator = Nominatim(user_agent="mi_aplicacion_geocodificador")
        # address = "Avenida Ignacio Carrera Pinto 397, Illapel, Coquimbo, Chile"

        try:
            # Geocodificar la dirección
            # location = geolocator.geocode(address)

            # Verificar si se obtuvo una ubicación

            self.lat = -30.0000000
            self.lon = -71.0000000

            # Inicializar y mostrar el mapa con las coordenadas
            self.map_view = MapaApp(self.lat, self.lon)
            self.map_view.show()

        except Exception as e:
            print(f"Ocurrió un error durante la geocodificación: {e}")

    def gain(self):
        self.view_gain_view = Viewmaingain()
        self.view_gain_view.show()

    def report(self):
        id_user = self.id_user
        self.view_report = Viewmainreport(id_user)
        self.view_report.show()

    def employee(self):
        self.view_employee = Viewmainemployee()
        self.view_employee.show()

    def calendar(self):
        self.view_calendar = Viewmaincalendar()
        self.view_calendar.show()

    def graphi_income(self):
        self.view_graphic_income = SaleChart()
        self.view_graphic_income.show()

    def graphi_expenses(self):
        self.view_graphic_expenses = ExpensesChart()
        self.view_graphic_expenses.show()

    def graphi_investment(self):
        self.view_graphic_investement = InvestmentChart()
        self.view_graphic_investement.show()

    def graphi_transaction(self):
        self.view_graphic_transaction = TransactionChart()
        self.view_graphic_transaction.show()

    def graphi_gain(self):
        self.view_graphic_gain = GainChart()
        self.view_graphic_gain.show()

    def reload_ui(self):
        # Cambia el tema sin cerrar la ventana
        loadUi(f"design/admin/dashboardadmin{self.theme}.ui", self)

    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__(self.id_user)  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = Viewdashboradadmin()
    mi_app.show()
    sys.exit(app.exec_())
