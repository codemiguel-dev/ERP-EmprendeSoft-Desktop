import os
from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database


class ModelClient:

    def register(self, name, lastname, email, fono, address, client_type, image):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Verifica si el cliente ya existe
                    cur.execute("SELECT * FROM client WHERE name = ?", (name,))
                    user_data = cur.fetchone()
                    if user_data:
                        show_message("Error", "El cliente ya existe.")
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

                        # Inserta el cliente en la base de datos
                        cur.execute(
                            "INSERT INTO client (image, name, lastname, email, phone, address, type_client) VALUES (?, ?, ?, ?, ?, ?, ?);",
                            (
                                image_data,
                                name,
                                lastname,
                                email,
                                fono,
                                address,
                                client_type,
                            ),
                        )

                        show_message("Información", "Registro exitoso.")
                        # Opcional: abrir la ventana principal
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM client")
        trans = cursor.fetchall()
        conn.close()

        return trans

    def update(self, uid, name, lastname, email, fono, address, client_type, image):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Actualiza los datos del inventario existente

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

                    cur.execute(
                        """
                    UPDATE client
                    SET name = ?, lastname = ?, email = ?, phone = ?, address = ?, type_client = ?, image = ?
                    WHERE id = ?;
                    """,
                        (
                            name,
                            lastname,
                            email,
                            fono,
                            address,
                            client_type,
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
                    cur.execute("DELETE FROM client WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
