import sys

from PyQt5.QtWidgets import QApplication

from view.admin.maps.viewmaps import MapaApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MapaApp(0, 0)  # Puedes cambiar 0, 0 por coordenadas reales
    ventana.show()
    sys.exit(app.exec_())
