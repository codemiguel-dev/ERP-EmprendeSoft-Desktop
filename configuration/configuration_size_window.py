from PyQt5 import QtCore, QtGui, QtWidgets


def set_default_size_and_center(self):
    default_width = 600
    default_height = 650
    self.setFixedSize(default_width, default_height)
    # Obtener el tamaño de la pantalla
    screen = (
        QtWidgets.QDesktopWidget().screenGeometry()
    )  # Calcular las coordenadas para centrar la ventana
    x = (screen.width() - default_width) // 2
    y = (screen.height() - default_height) // 2
    self.move(x, y)
