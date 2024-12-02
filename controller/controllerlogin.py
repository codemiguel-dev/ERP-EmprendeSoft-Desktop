from PyQt5.QtWidgets import QMessageBox

from models.modellogin import Login


class LoginController:
    def __init__(self, view):
        self.model = Login()
        self.view = view

    def verify_credentials(self, username, userpassword):
        if not username or not userpassword:
            QMessageBox.information(
                self.view, "Mensaje", "Debe ingresar su cuenta y contraseña."
            )
            return False

        return self.model.loginadmin(username, userpassword)
