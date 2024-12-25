import os

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QSizeGrip
from PyQt5.uic import loadUi

from configuration.configuration_buttom import (
    icon_configurate_top,
    icon_excel,
    icon_exit_program,
)
from configuration.configuration_buttom_top import (
    control_bt_maximizar,
    control_bt_minimizar,
    control_bt_normal,
)
from configuration.configuration_config_theme import load_config
from configuration.configuration_delete_banner import delete_banner
from configuration.configuration_window_move import mousePressEvent, window_move
from controller.controlleruser import UserController


class Viewmainuserprofile(QtWidgets.QMainWindow):
    def __init__(self, id_user):
        super(Viewmainuserprofile, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/standar/mainuserprofile{self.theme}.ui", self)

        self.id_user = id_user

        icon_exit_program(self)
        icon_configurate_top(self)
        delete_banner(self)

        # Inicializar el QSizeGrip y establecer su tamaño
        self.gripSize = 16  # Define el tamaño del grip
        self.grip = QSizeGrip(self)  # Crea un QSizeGrip para el redimensionamiento
        self.grip.resize(self.gripSize, self.gripSize)  # Ajusta el tamaño del QSizeGrip

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
        self.btn_update_profile.clicked.connect(self.update_profile)
        self.btn_add_image.clicked.connect(self.add_image)
        self.bt_maximizar.hide()

        self.controlleruser = UserController(self)
        self.get_user()

    def close_program(self):
        QApplication.quit()

    def get_user(self):
        # Llama al controlador para obtener los datos del usuario por ID
        user = self.controlleruser.search_user(self.id_user)

        if user:
            # Asumiendo que el resultado es una tupla (id, nombre, correo, etc.)
            self.nametxt.setText(user[2])  # Campo para el nombre
            self.emailtxt.setText(user[4])  # Campo para el correo
            self.phonetxt.setText(user[5])
        else:
            QMessageBox.warning(self, "Error", "Usuario no encontrado")

    def add_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Imagen",
            "",
            "Images (*.png *.xpm *.jpg);;All Files (*)",
            options=options,
        )
        if file_path:
            self.imagetxt.setText(file_path)  # Mostrar el path de la imagen (opcional)

            # Crear un QPixmap con la imagen seleccionada
            pixmap = QPixmap(file_path)

            # Ajustar el tamaño del QLabel y permitir que la imagen se escale
            self.image_label.setFixedSize(
                200, 200
            )  # Cambiar el tamaño del QLabel (ancho, alto)
            self.image_label.setScaledContents(
                True
            )  # La imagen se escala al tamaño del QLabel

            # Mostrar la imagen en el QLabel
            self.image_label.setPixmap(pixmap)

            # Centrar la imagen dentro del QLabel
            self.image_label.setAlignment(
                Qt.AlignCenter
            )  # Centrar horizontal y verticalmente

    def update_profile(self):
        name = self.nametxt.text()
        password = self.passwordtxt.text()
        password2 = self.passwordtxt2.text()
        email = self.emailtxt.text()
        phone = self.phonetxt.text()

        # Validar que las contraseñas coincidan
        if password != password2:
            QMessageBox.warning(
                self,
                "Advertencia",
                "Las contraseñas no coinciden. Por favor, intente de nuevo.",
            )
            return

        if not name or not email or not phone:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controlleruser.update_profile(self.id_user, name, email, phone, password)
