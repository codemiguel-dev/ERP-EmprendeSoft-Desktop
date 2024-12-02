import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from view.viewlogin import LoginView


class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.showMessage("Cargando...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear y mostrar el splash screen
    pixmap = QPixmap("img/icon.png")  # Ruta a tu imagen de splash
    splash = SplashScreen(pixmap)
    splash.show()

    view = LoginView()

    # Mostrar la ventana principal después de un retraso
    QTimer.singleShot(
        3000, splash.close
    )  # El splash screen se mostrará durante 3 segundos
    QTimer.singleShot(
        3000, view.show
    )  # Mostrar la ventana principal después de 3 segundos

    sys.exit(app.exec_())
