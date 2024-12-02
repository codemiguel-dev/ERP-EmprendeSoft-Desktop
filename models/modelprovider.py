import os
from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database


class ModelProvider:

    def register(self, rut, name, email, fono, address, type_provider, image):
        conn = connect_to_database()
        if conn:
            conn.execute(
                "PRAGMA busy_timeout = 3000"
            )  # Espera hasta 3 segundos antes de fallar por bloqueo
            try:
                with conn:
                    cur = conn.cursor()

                    # Verifica si el usuario ya existe
                    cur.execute("SELECT * FROM provider WHERE name = ?", (name,))
                    user_data = cur.fetchone()
                    if user_data:
                        show_message("Error", "El proveedor ya existe.")
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

                        # Inserta el nuevo usuario en la base de datos
                        cur.execute(
                            "INSERT INTO provider (image, rut, name, email, phone, address, type) VALUES (?, ?, ?, ?, ?, ?, ?);",
                            (
                                image_data,
                                rut,
                                name,
                                email,
                                fono,
                                address,
                                type_provider,
                            ),
                        )

                        show_message("Información", "Registro exitoso.")
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM provider")
        user = cursor.fetchall()
        conn.close()

        return user

    def update(self, uid, rut, name, email, fono, address, type_provider, image):
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

                    # Actualiza los datos del inventario existente
                    cur.execute(
                        """
                    UPDATE provider 
                    SET rut = ?, name = ?, email = ?, phone = ?, address = ?, type = ?, image =?
                    WHERE id = ?;
                    """,
                        (
                            rut,
                            name,
                            email,
                            fono,
                            address,
                            type_provider,
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
                    cur.execute("DELETE FROM provider WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
