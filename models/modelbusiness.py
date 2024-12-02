import os
import sqlite3
from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database
from view.standar.viewdashboard import Viewdashboardstandar


class ModelBusiness:

    def register(
        self,
        address_id,
        name,
        image,
        legal_form,
        industry,
        registration_number,
        founding_date,
    ):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Verificar si ya existe una fila en la tabla `business`
                    cur.execute("SELECT COUNT(*) FROM business")
                    business_count = cur.fetchone()[0]

                    # Si ya existe una fila, impedir registrar una nueva
                    if business_count >= 1:
                        show_message(
                            "Advertencia", "Solo se puede registrar una empresa."
                        )
                        return

                    # Si se ha proporcionado una imagen
                    if image:
                        try:
                            # Verifica que la imagen sea una ruta de archivo válida
                            if not os.path.isfile(image):
                                raise FileNotFoundError(
                                    "La imagen seleccionada no se encontró."
                                )
                            with open(image, "rb") as file:
                                image_data = file.read()

                            # Crear el directorio si no existe
                            # img_directory = 'img/business/'
                            # os.makedirs(img_directory, exist_ok=True)

                            # Obtener el nombre de la imagen
                            # image_name = os.path.basename(image)
                            # new_image_path = os.path.join(img_directory, image_name)

                            # Mover la imagen a la carpeta especificada
                            # shutil.copy(image, new_image_path)

                            # Guardar la ruta de la imagen en la base de datos
                            # image_link = new_image_path  # Ruta de la imagen para guardar en la base de datos
                        except FileNotFoundError:
                            show_message(
                                "Error", "La imagen seleccionada no se encontró."
                            )
                            return
                    else:
                        image_data = (
                            None  # O carga una imagen por defecto si lo prefieres
                        )

                    # Insertar el nuevo registro de empresa
                    cur.execute(
                        """
                        INSERT INTO business (address_id, name, image, legal_form, industry, registration_number, founding_date) 
                        VALUES (?, ?, ?, ?, ?, ?, ?);
                        """,
                        (
                            address_id,
                            name,
                            image_data,
                            legal_form,
                            industry,
                            registration_number,
                            founding_date,
                        ),
                    )

                    show_message("Información", "Registro exitoso.")
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def register_gain(self, gain):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    gain = float(gain)
                    # Obtener el ID de la empresa
                    cur.execute("SELECT id FROM business LIMIT 1")
                    business_id = cur.fetchone()
                    if business_id:
                        business_id = business_id[
                            0
                        ]  # Actualizar el registro existente con el nuevo valor de gain
                        cur.execute(
                            """ UPDATE business SET gain = ? WHERE id = ?; """,
                            (gain, business_id),
                        )
                        show_message(
                            "Información", "Ganancia actualizada en la base de datos"
                        )
                    else:
                        show_message(
                            "Error", "No se encontró la empresa en la base de datos."
                        )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get_graphi(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT name, gain FROM business;")
        inv = cursor.fetchall()
        conn.close()

        return inv

    def get(self):
        conn = connect_to_database()
        cursor = conn.cursor()

        # INNER JOIN entre business y address
        cursor.execute(
            """
        SELECT 
            business.id, 
            business.name,
            business.image, 
            business.legal_form, 
            business.industry, 
            business.registration_number, 
            business.founding_date,
            address.id, 
            address.country, 
            address.region,
            address.commune,           
            address.description
        FROM 
            business
        INNER JOIN 
            address 
        ON 
            business.address_id = address.id;
        """
        )

        business = cursor.fetchall()  # Obtener todos los resultados de la consulta
        conn.close()

        return business

    def update(
        self,
        id_goal,
        name,
        num_legal,
        industry,
        num_register,
        date_founding,
        address,
        image,
    ):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    if (
                        image
                    ):  # Leer la imagen como binario solo si la imagen no es nula
                        with open(image, "rb") as file:
                            image_data = (
                                file.read()
                            )  # Actualiza los datos del inventario existente incluyendo la imagen
                            cur.execute(
                                """ UPDATE business SET name = ?, legal_form = ?, industry = ?, registration_number = ?, founding_date = ?, address_id = ?, image = ? WHERE id = ?; """,
                                (
                                    name,
                                    num_legal,
                                    industry,
                                    num_register,
                                    date_founding,
                                    address,
                                    image_data,
                                    id_goal,
                                ),
                            )
                    else:  # Actualiza los datos del inventario existente sin la imagen
                        cur.execute(
                            """ UPDATE business SET name = ?, legal_form = ?, industry = ?, registration_number = ?, founding_date = ?, address_id = ? WHERE id = ?; """,
                            (
                                name,
                                num_legal,
                                industry,
                                num_register,
                                date_founding,
                                address,
                                id_goal,
                            ),
                        )
                        conn.commit()
                        show_message(
                            "Información",
                            "Actualización realizada en la base de datos.",
                        )

            except sqlite3.Error as e:
                show_message(
                    "Error", f"No se pudo actualizar la base de datos: {e}"
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
                    cur.execute("DELETE FROM business WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
