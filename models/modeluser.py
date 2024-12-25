import os

import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from configuration.configuration_message import show_message
from models.connect import connect_to_database


class ModelUser:

    def register(self, name, email, fono, address, password, role, image):
        conn = connect_to_database()
        if conn:
            conn.execute(
                "PRAGMA busy_timeout = 3000"
            )  # Espera hasta 3 segundos antes de fallar por bloqueo
            try:
                with conn:
                    cur = conn.cursor()

                    # Verifica si el usuario ya existe
                    cur.execute("SELECT * FROM user WHERE name = ?", (name,))
                    user_data = cur.fetchone()
                    if user_data:
                        show_message("Error", "El usuario ya existe.")
                    else:
                        # Si se ha proporcionado una imagen
                        if image:
                            try:
                                # Verifica que image sea una ruta de archivo válida
                                if not os.path.isfile(image):
                                    raise FileNotFoundError(
                                        "La imagen seleccionada no se encontró."
                                    )
                                with open(image, "rb") as file:
                                    image_data = file.read()
                            except FileNotFoundError:
                                show_message(
                                    "Error", "La imagen seleccionada no se encontró."
                                )
                                return
                        else:
                            image_data = None  # O puedes cargar una imagen por defecto

                        # Cifra la contraseña antes de almacenarla
                        hashed_password = bcrypt.hashpw(
                            password.encode("utf-8"), bcrypt.gensalt()
                        )

                        # Inserta el nuevo usuario en la base de datos
                        cur.execute(
                            "INSERT INTO user (image, name, password, email, contact_num, address, role) VALUES (?, ?, ?, ?, ?, ?, ?);",
                            (
                                image_data,
                                name,
                                hashed_password,
                                email,
                                fono,
                                address,
                                role,
                            ),
                        )

                        show_message("Información", "Registro exitoso.")
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get_user(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        user = cursor.fetchall()
        conn.close()

        return user

    def update(self, uid, name, password, email, fono, address, role, image):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Si se ha proporcionado una imagen
                    if image:
                        try:
                            # Verifica que image sea una ruta de archivo válida
                            if not os.path.isfile(image):
                                raise FileNotFoundError(
                                    "La imagen seleccionada no se encontró."
                                )
                            with open(image, "rb") as file:
                                image_data = file.read()
                        except FileNotFoundError:
                            show_message(
                                "Error", "La imagen seleccionada no se encontró."
                            )
                            return
                    else:
                        image_data = None  # O puedes cargar una imagen por defecto

                    # Cifra la contraseña antes de almacenarla
                    hashed_password = bcrypt.hashpw(
                        password.encode("utf-8"), bcrypt.gensalt()
                    )

                    # Actualiza los datos del inventario existente
                    cur.execute(
                        """
                    UPDATE user 
                    SET name = ?, password = ?, email = ?, contact_num = ?, address = ?, role = ?, image =?
                    WHERE id = ?;
                    """,
                        (
                            name,
                            hashed_password,
                            email,
                            fono,
                            address,
                            role,
                            image_data,
                            uid,
                        ),
                    )

                    show_message(
                        "Información", "Actualización realizada en la base de datos."
                    )

            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def delete(self, uid):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Elimina el registro del inventario existente
                    cur.execute("DELETE FROM user WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get_user_by_id(self, user_id):
        conn = connect_to_database()  # Conecta a la base de datos
        cursor = conn.cursor()

        # Consulta SQL para buscar un usuario por su ID
        query = "SELECT * FROM user WHERE id = ?"
        cursor.execute(query, (user_id,))

        # Obtén el usuario (asumiendo que `id` es único)
        user = cursor.fetchone()  # Usa fetchone() para un solo resultado

        conn.close()  # Cierra la conexión
        return user  # Devuelve el usuario encontrado o None si no existe

    def update_profile(self, user_id, name, email, phone, password_new, image):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    if image:
                        try:
                            # Verifica que image sea una ruta de archivo válida
                            if not os.path.isfile(image):
                                raise FileNotFoundError(
                                    "La imagen seleccionada no se encontró."
                                )
                            with open(image, "rb") as file:
                                image_data = file.read()
                        except FileNotFoundError:
                            show_message(
                                "Error", "La imagen seleccionada no se encontró."
                            )
                            return
                    else:
                        image_data = None  # O puedes cargar una imagen por defecto

                    # Cifra la contraseña antes de almacenarla
                    hashed_password = bcrypt.hashpw(
                        password_new.encode("utf-8"), bcrypt.gensalt()
                    )

                    # Actualiza los datos del inventario existente
                    cur.execute(
                        """
                    UPDATE user 
                    SET name = ?, password = ?, email = ?, contact_num = ?, image = ?
                    WHERE id = ?;
                    """,
                        (
                            name,
                            hashed_password,
                            email,
                            phone,
                            image_data,
                            user_id,
                        ),
                    )

                    show_message(
                        "Información", "Actualización realizada en la base de datos."
                    )

            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
