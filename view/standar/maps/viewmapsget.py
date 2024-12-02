import json
import os
import sys

from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow


class CoordinateHandler(QObject):
    coordinatesReceived = pyqtSignal(
        list
    )  # Signal para emitir las coordenadas a JavaScript

    @pyqtSlot(list, float, float)
    def updateCoordinates(self, updatedCoordinates, lat, lon):
        # Obtener la ruta del directorio actual o del ejecutable
        if hasattr(sys, "_MEIPASS"):
            current_dir = sys._MEIPASS
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Crear la ruta completa del archivo HTML del mapa
        data_json = os.path.join(current_dir, "html/json/coordinate.json")

        file_path = data_json
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Filter out the coordinate to remove
        existing_data = [
            coord
            for coord in existing_data
            if not (coord["latitude"] == lat and coord["longitude"] == lon)
        ]

        # Save the updated coordinates
        with open(file_path, "w") as file:
            json.dump(existing_data, file, indent=4)

        print(f"Coordenada eliminada: Latitud: {lat}, Longitud: {lon}")


class MapsAppGet(QMainWindow):
    def __init__(self):
        super(MapsAppGet, self).__init__()
        self.webView = QWebEngineView(self)
        self.setCentralWidget(self.webView)
        self.resize(800, 600)
        # Obtener la ruta del directorio actual o del ejecutable
        if hasattr(sys, "_MEIPASS"):
            current_dir = sys._MEIPASS
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Crear la ruta completa del archivo HTML del mapa
        mapa_html = os.path.join(current_dir, "html/mapa_get_coordinate.html")
        url_base = QUrl.fromLocalFile(mapa_html)
        self.webView.setUrl(url_base)

        self.channel = QWebChannel()
        self.coordinate_handler = CoordinateHandler()
        self.channel.registerObject("pyqtObj", self.coordinate_handler)
        self.webView.page().setWebChannel(self.channel)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MapsAppGet()
    ventana.show()
    sys.exit(app.exec_())
