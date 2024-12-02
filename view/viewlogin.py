from PyQt5.QtWidgets import QMainWindow, QLineEdit, QSizeGrip, QApplication, QMessageBox
from PyQt5.QtGui import QIcon, QCursor
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from controller.controllerlogin import LoginController
from view.viewregister import RegisterForm # type: ignore
import configparser

class LoginView(QMainWindow):
    def __init__(self):
        super(LoginView, self).__init__()
        self.theme = self.load_config()  # Lee la configuración al iniciar
        loadUi(f'design/designlogin{self.theme}.ui', self)
        self.init_ui()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('Settings', 'theme', fallback='0')

    def save_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if 'Settings' not in config:
            config.add_section('Settings')
        
        config.set('Settings', 'theme', self.theme)
        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def init_ui(self):
        self.bt_minimize.setIcon(QIcon('img/minus.svg')) 
        self.bt_maximize.setIcon(QIcon('img/chevron-down.svg'))
        self.bt_normal.setIcon(QIcon('img/chevron-up.svg')) 
        self.bt_close.setIcon(QIcon('img/x.svg'))
        self.btn_icon.setIcon(QIcon('img/icon.png'))

        self.bt_minimize.clicked.connect(self.showMinimized)
       
        self.bt_normal.clicked.connect(self.control_bt_normal)
        self.bt_maximize.clicked.connect(self.control_bt_maximize)
        self.bt_close.clicked.connect(self.close)
        self.btn_register.clicked.connect(self.abrir_formulario_registro)
        self.btn_login.clicked.connect(self.login)
        self.passwordtxt.returnPressed.connect(self.login) # Agrega esta línea

        self.bt_normal.hide()
        self.click_posicion = None

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        icon_user = QIcon("img/user.svg")
        icon_lock = QIcon("img/lock.svg")
        self.nametxt.addAction(icon_user, QLineEdit.LeadingPosition)
        self.passwordtxt.addAction(icon_lock, QLineEdit.LeadingPosition)

        self.gripSize = 10
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        self.bt_minimize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_normal.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_maximize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_close.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.controller = LoginController(self)

    
    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__()  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana

    def control_bt_normal(self):
        self.showNormal()
        self.bt_normal.hide()
        self.bt_maximize.show()

    def control_bt_maximize(self):
        self.showMaximized()
        self.bt_maximize.hide()
        self.bt_normal.show()

    def mousePressEvent(self, event):
        self.click_posicion = event.globalPos()

    def mover_ventana(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()

        if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normal.show()
        else:
            self.showNormal()
            self.bt_normal.hide()
            self.bt_maximize.show()

    def abrir_formulario_registro(self):
        self.register_form = RegisterForm()
        self.register_form.show()

    def login(self):
        username = self.nametxt.text()
        password = self.passwordtxt.text()
        if self.controller.verify_credentials(username, password):
            self.close()  # Cierra la ventana de login si el inicio de sesión es exitoso
