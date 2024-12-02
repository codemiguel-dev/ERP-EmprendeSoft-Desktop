# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelregister import Register


class RegisterController:
    def __init__(self, view):
        self.model = Register()
        self.view = view

    def register_user(self, username, userpassword, email, contact_num, address, role):
        self.model.register(username, userpassword, email, contact_num, address, role)
