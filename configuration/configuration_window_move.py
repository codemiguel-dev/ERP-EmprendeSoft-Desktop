from PyQt5 import QtCore


def mousePressEvent(self, event):
    # Capturar posición de click para mover la ventana
    self.clickPosition = event.globalPos()


def window_move(self, event):
    # Mover la ventana si no está maximizada
    if not self.isMaximized() and event.buttons() == QtCore.Qt.LeftButton:
        self.move(self.pos() + event.globalPos() - self.clickPosition)
        self.clickPosition = event.globalPos()
        event.accept()

    if event.globalPos().y() <= 20:
        self.showMaximized()
    else:
        self.showNormal()
