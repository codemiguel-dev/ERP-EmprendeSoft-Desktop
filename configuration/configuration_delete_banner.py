from PyQt5 import QtCore


def delete_banner(self):
    # Eliminar barra de título y hacer la ventana translúcida
    self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    self.setWindowOpacity(1)
