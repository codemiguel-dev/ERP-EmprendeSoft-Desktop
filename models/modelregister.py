from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database
from view.standar.viewdashboard import Viewdashboardstandar


class Register:

    def register(self, username, userpassword, email, contact_num, address, role):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Verifica si el usuario ya existe
                    cur.execute("SELECT * FROM user WHERE name = ?", (username,))
                    user_data = cur.fetchone()

                    if user_data:
                        show_message("Error", "El usuario ya existe.")
                    else:
                        # Cifra la contraseña antes de almacenarla
                        hashed_password = bcrypt.hashpw(
                            userpassword.encode("utf-8"), bcrypt.gensalt()
                        )
                        role = "standar"

                        # Inserta el nuevo usuario en la base de datos
                        cur.execute(
                            "INSERT INTO user (name, email, contact_num, address, password, role) VALUES (?, ?, ?, ?, ?, ?);",
                            (
                                username,
                                email,
                                contact_num,
                                address,
                                hashed_password,
                                role,
                            ),
                        )

                        show_message("Información", "Registro exitoso.")

                        self.dashboard_view = Viewdashboardstandar()
                        self.dashboard_view.show()
                        # Opcional: abrir la ventana principal
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
