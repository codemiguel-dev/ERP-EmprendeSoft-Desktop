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

        # Validar longitud mínima del nombre de usuario
        if len(username) < 3:
            QMessageBox.warning(
                self.view,
                "Mensaje",
                "El nombre de usuario debe tener al menos 3 caracteres.",
            )
            return False

        # Validar caracteres no permitidos en el nombre de usuario
        # if not username.isalnum():
        #    QMessageBox.warning(
        #        self.view,
        #         "Mensaje",
        #        "El nombre de usuario solo debe contener caracteres alfanuméricos.",
        #    )
        #    return False

        # Validar longitud mínima de la contraseña
        if len(userpassword) < 3:
            QMessageBox.warning(
                self.view, "Mensaje", "La contraseña debe tener al menos 3 caracteres."
            )
            return False

        # Validar fortaleza de la contraseña (opcional)
        # if not any(char.isdigit() for char in userpassword) or not any(
        #    char.isalpha() for char in userpassword
        # ):
        #    QMessageBox.warning(
        #        self.view, "Mensaje", "La contraseña debe incluir letras y números."
        #    )
        #    return False

        return self.model.loginadmin(username, userpassword)
