from passlib.hash import bcrypt as passlib_bcrypt
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QMessageBox, QSizeGrip

from models.connect import connect_to_database
from view.admin.viewdashboard import Viewdashboradadmin
from view.standar.viewdashboard import Viewdashboardstandar


class Login:
    def loginadmin(self, username, userpassword):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    find_user = (
                        "SELECT id, name, password, role FROM user WHERE name = ?"
                    )
                    cur.execute(find_user, [username])
                    user_data = cur.fetchone()
                    id_user = user_data[0]

                    if user_data:
                        stored_password_hash = user_data[2]
                        if passlib_bcrypt.verify(userpassword, stored_password_hash):
                            if user_data[3] == "administrador":
                                self.dashboard_view = Viewdashboradadmin(id_user)
                                self.dashboard_view.show()
                            elif user_data[3] == "standar":
                                self.dashboard_view = Viewdashboardstandar()
                                self.dashboard_view.show()
                            return True
                        else:
                            QMessageBox.critical(
                                None, "Error", "Contraseña incorrecta."
                            )  # Usa None como primer argumento
                    else:
                        QMessageBox.critical(
                            None, "Error", "Cuenta incorrecta."
                        )  # Usa None como primer argumento
            finally:
                conn.close()
        else:
            QMessageBox.critical(
                None, "Error", "No se pudo conectar a la base de datos."
            )  # Usa None como primer argumento
        return False
