import json
import os
import sys
import uuid

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QMessageBox, QSizeGrip
from PyQt5.uic import loadUi

from configuration.configuration_buttom import icon_configurate_top, icon_exit_program
from configuration.configuration_buttom_top import (
    control_bt_maximizar,
    control_bt_minimizar,
    control_bt_normal,
)
from configuration.configuration_config_theme import load_config
from controller.controlleraddress import AddressController
from controller.controllercoordinate import CoordinateController
from view.admin.maps.viewmapsget import MapsAppGet


class CoordinateHandler(QObject):
    coordinatesReceived = pyqtSignal(list)  # Crear un nuevo signal

    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lon):
        print(f"Coordenadas clicadas: Latitud: {lat}, Longitud: {lon}")

        # Emitir las coordenadas para que sean manejadas por MapaApp
        self.coordinatesReceived.emit([lat, lon])


class MapaApp(QMainWindow):
    def __init__(self, latitud, longitud):
        super(MapaApp, self).__init__()
        self.theme = load_config(self)  # Leer configuración al iniciar
        loadUi(
            f"design/admin/mainmap{self.theme}.ui", self
        )  # Cargar diseño de Qt Designer

        icon_exit_program(self)
        icon_configurate_top(self)

        # Configuración de la ventana
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        self.gripSize = 16
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        self.showMaximized()

        # Control de botones de la barra de títulos
        self.bt_minimizar.clicked.connect(lambda: control_bt_minimizar(self))
        self.bt_restaurar.clicked.connect(lambda: control_bt_normal(self))
        self.bt_maximizar.clicked.connect(lambda: control_bt_maximizar(self))
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_maximizar.hide()

        self.btn_get.clicked.connect(self.mapsget)

        # Obtener la ruta del directorio actual o del ejecutable
        if hasattr(sys, "_MEIPASS"):
            current_dir = sys._MEIPASS
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Crear la ruta completa del archivo HTML del mapa
        mapa_html = os.path.join(current_dir, "html/mapa.html")
        url_base = QUrl.fromLocalFile(mapa_html)  # Agregar las coordenadas a la URL
        latitud = -33.4569
        longitud = -70.6483
        url_con_coordenadas = url_base.toString() + f"?lat={latitud}&lon={longitud}"
        self.channel = QWebChannel()
        self.coordinate_handler = CoordinateHandler()
        self.channel.registerObject("pyqtObj", self.coordinate_handler)

        self.webView.page().setWebChannel(self.channel)
        self.webView.setUrl(QUrl(url_con_coordenadas))

        # Campos de texto para mostrar las coordenadas
        self.lattxt = self.findChild(QLineEdit, "lattxt")
        self.lontxt = self.findChild(QLineEdit, "lontxt")

        if self.lattxt is None or self.lontxt is None:
            print(
                "Error: No se encontraron los campos de texto 'lattxt' y 'lontxt'. Verifica los IDs en tu archivo .ui"
            )
            return

        self.lattxt.setText("")
        self.lontxt.setText("")

        # Conectar la señal
        self.coordinate_handler.coordinatesReceived.connect(self.addCoordinate)

        # Conectar el botón
        self.btn_add.clicked.connect(self.triggerMessage)
        self.btn_exit.clicked.connect(self.close_program)

        # Almacenar todas las coordenadas
        self.coordinates = []

        # get json
        self.cargar_datos_json_color()
        self.cargar_datos_json_status()

        self.controlleraddress = AddressController(self)
        self.controllercoordinate = CoordinateController(self)

        self.show_address()

    def close_program(self):
        QApplication.quit()

    @pyqtSlot(list)
    def addCoordinate(self, coordinates):
        self.coordinates.append({"lat": coordinates[0], "long": coordinates[1]})
        self.saveCoordinates(coordinates)
        print(
            f"Coordenadas guardadas: Latitud: {coordinates[0]}, Longitud: {coordinates[1]}"
        )  # Mostrar en print

    def updateTexts(self, lat, lon):
        self.lattxt.setText(f"{lat:.5f}")
        self.lontxt.setText(f"{lon:.5f}")

    def saveCoordinates(self, coordinates):
        # Actualizar los campos de texto con la nueva coordenada
        self.lattxt.setText(f"{coordinates[0]:.5f}")
        self.lontxt.setText(f"{coordinates[1]:.5f}")

        # Añadir nueva coordenada
        self.coordinates.append({"lat": coordinates[0], "long": coordinates[1]})

        # Guardar todas las coordenadas en coordenadas_guardadas.json
        if self.coordinates:
            with open("coordenadas_guardadas.json", "w") as f:
                json.dump(self.coordinates, f, indent=4)
            print("Coordenadas guardadas en coordenadas_guardadas.json")

    def triggerMessage(self):
        lat = self.lattxt.text()
        lon = self.lontxt.text()
        if not lat or not lon:
            self.show_message(
                "Error", "Todos los campos son obligatorios.", QMessageBox.Critical
            )
            return

        lat = float(lat)
        lon = float(lon)

        self.message(lat, lon)

    def message(self, lat, lon):
        print(f"Coordenadas clicadas: Latitud: {lat}, Longitud: {lon}")

        # Guardar la última coordenada en coordenada.json
        if os.path.exists("json/coordinate.json"):
            with open("json/coordinate.json", "r") as f:
                existing_coordinates = json.load(f)
            if isinstance(existing_coordinates, dict):
                existing_coordinates = [
                    existing_coordinates
                ]  # Convertir dict en una lista si es necesario
        else:
            existing_coordinates = []

        address_id = self.address_combobox.currentData()

        color = self.colorcombobox.currentText()
        description = self.descriptiontxt.toPlainText()
        status = self.statuscombobox.currentText()

        if not color or not description or not status or not lat or not lon:
            self.show_message(
                "Error", "Todos los campos son obligatorios.", QMessageBox.Critical
            )
            return

        # Generar un ID único para la nueva coordenada
        coordinate_id = str(uuid.uuid4())

        # Añadir nueva coordenada
        existing_coordinates.append(
            {
                "id": coordinate_id,
                "latitude": lat,
                "longitude": lon,
                "color": color,
                "description": description,
                "status": status,
            }
        )
        if hasattr(sys, "_MEIPASS"):
            current_dir = sys._MEIPASS
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Crear la ruta completa del archivo HTML del mapa
        data_json = os.path.join(current_dir, "html/json/coordinate.json")
        with open(data_json, "w") as f:
            json.dump(existing_coordinates, f, indent=4)

        print("Última coordenada guardada en coordenada.json")

        return self.controllercoordinate.register(address_id, coordinate_id, lat, lon)

    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__()  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana

    def mapsget(self):
        self.view_maps_get = MapsAppGet()
        self.view_maps_get.show()

    def cargar_datos_json_color(self):
        try:
            # Abre el archivo JSON
            with open("json/color.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("color", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                # Agregar los nombres de las regiones al QComboBox
                for color in names:
                    self.colorcombobox.addItem(color["name"])

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

    def cargar_datos_json_status(self):
        try:
            # Abre el archivo JSON
            with open("json/status_send.json", "r", encoding="utf-8") as archivo_json:
                self.datos = json.load(
                    archivo_json
                )  # Guardar los datos JSON en self.datos
                names = self.datos.get("status", [])

                if not names:
                    raise ValueError("No se encontraron datos en 'name'")

                # Agregar los nombres de las regiones al QComboBox
                for status in names:
                    self.statuscombobox.addItem(status["name"])

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

    def show_address(self):
        # Desconectar la señal para evitar bucles infinitos
        self.address_combobox.blockSignals(True)

        self.address_combobox.clear()
        # Obtener datos de inventario desde el controlador
        address = self.controlleraddress.get()

        # Añadir datos al comboBox
        for a in address:
            uid = a[0]  # El primer elemento es el ID del producto
            country = a[1]  # El segundo elemento es el país
            region = a[2]  # El tercer elemento es la región
            commune = a[3]
            description = a[4]

            # Concatenar country y region en una sola cadena
            address_str = f"{country} - {region} - {commune} - {description}"

            # Añadir la concatenación de country y region al combobox
            self.address_combobox.addItem(address_str, uid)

        # Reconectar la señal después de añadir los datos
        self.address_combobox.blockSignals(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Inicializar la aplicación con coordenadas
    ventana = MapaApp(0, 0)  # Puedes cambiar 0, 0 por coordenadas reales
    ventana.show()
    sys.exit(app.exec_())
