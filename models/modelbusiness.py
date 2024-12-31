import os
import sqlite3

import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from configuration.configuration_message import show_message
from models.connect import connect_to_database


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

                    # Inicializa los valores a actualizar y los parámetros
                    insert_fields = []
                    params = []

                    if address_id is not None:
                        insert_fields.append("address_id")
                        params.append(address_id)

                    if name is not None:
                        insert_fields.append("name")
                        params.append(name)

                    if image:
                        try:
                            # Verifica que la imagen sea una ruta válida
                            if not os.path.isfile(image):
                                raise FileNotFoundError(
                                    "La imagen seleccionada no se encontró."
                                )
                            with open(image, "rb") as file:
                                image_data = sqlite3.Binary(file.read())
                            insert_fields.append("image")
                            params.append(image_data)
                        except FileNotFoundError:
                            show_message(
                                "Error", "La imagen seleccionada no se encontró."
                            )
                            return

                    if legal_form is not None:
                        insert_fields.append("legal_form")
                        params.append(legal_form)

                    if industry is not None:
                        insert_fields.append("industry")
                        params.append(industry)

                    if registration_number is not None:
                        insert_fields.append("registration_number")
                        params.append(registration_number)

                    if founding_date is not None:
                        insert_fields.append("founding_date")
                        params.append(founding_date)

                    # Si hay campos para insertar
                    if insert_fields:
                        placeholders = ", ".join(["?"] * len(insert_fields))
                        insert_query = f"""
                            INSERT INTO business ({', '.join(insert_fields)})
                            VALUES ({placeholders});
                        """
                        cur.execute(insert_query, params)

                        show_message("Información", "Registro exitoso.")
                    else:
                        show_message(
                            "Información", "No se proporcionaron campos para registrar."
                        )

            except sqlite3.Error as e:
                show_message("Error", f"No se pudo registrar el producto: {e}")
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
        uid,
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

                    # Inicializa los valores a actualizar y los parámetros
                    update_fields = []
                    params = []

                    # Agrega los campos dinámicamente
                    if address is not None:
                        update_fields.append("address_id = ?")
                        params.append(address)

                    # Agrega los campos dinámicamente
                    if name is not None:
                        update_fields.append("name = ?")
                        params.append(name)

                    if image:
                        try:
                            # Verifica que la imagen sea una ruta válida
                            if not os.path.isfile(image):
                                raise FileNotFoundError(
                                    "La imagen seleccionada no se encontró."
                                )
                            with open(image, "rb") as file:
                                image_data = sqlite3.Binary(file.read())
                            update_fields.append("image = ?")
                            params.append(image_data)
                        except FileNotFoundError:
                            show_message(
                                "Error", "La imagen seleccionada no se encontró."
                            )
                            return

                    if num_legal is not None:
                        update_fields.append("legal_form = ?")
                        params.append(num_legal)

                    if industry is not None:
                        update_fields.append("industry = ?")
                        params.append(industry)

                    if num_register is not None:
                        update_fields.append("registration_number = ?")
                        params.append(num_register)

                    if date_founding is not None:
                        update_fields.append("founding_date = ?")
                        params.append(date_founding)

                    # Solo procede si hay campos para actualizar
                    if update_fields:
                        update_query = f"""
                            UPDATE business 
                            SET {', '.join(update_fields)}
                            WHERE id = ?;
                        """
                        params.append(uid)
                        cur.execute(update_query, params)

                        show_message(
                            "Información",
                            "Actualización realizada en la base de datos.",
                        )
                    else:
                        show_message(
                            "Información",
                            "No se realizaron cambios, todos los campos son nulos.",
                        )

            except sqlite3.Error as e:
                show_message("Error", f"No se pudo actualizar la base de datos: {e}")
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
