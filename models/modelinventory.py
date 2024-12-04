import sqlite3

import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from configuration.configuration_message import show_message
from models.connect import connect_to_database


class ModelInventory:

    def register(
        self,
        name,
        category,
        stock,
        purchase_price,
        sale_price,
        total_purch,
        description,
        image,
    ):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Leer la imagen como binario
                    with open(image, "rb") as file:
                        image_data = file.read()

                    # Inserta el nuevo usuario en la base de datos con la imagen como BLOB
                    cur.execute(
                        """
                        INSERT INTO inventory (name, category, stock, purchase_price, sale_price, totalpurch, description, image) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                        """,
                        (
                            name,
                            category,
                            stock,
                            purchase_price,
                            sale_price,
                            total_purch,
                            description,
                            image_data,
                        ),
                    )

                show_message("Información", "Registro exitoso.")
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get_inventory(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        inventory = cursor.fetchall()
        conn.close()

        return inventory

    def update(
        self,
        uid,
        name,
        category,
        stock,
        purchase_price,
        sale_price,
        totalpurch,
        description,
        image_path,
    ):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Obtener la imagen actual del inventario antes de la actualización
                    cur.execute("SELECT image FROM inventory WHERE id = ?", (uid,))
                    current_image_blob = cur.fetchone()[0]

                    # Convertir la imagen a BLOB si no es None
                    if image_path:
                        with open(image_path, "rb") as image_file:
                            image_blob = sqlite3.Binary(image_file.read())
                    else:
                        image_blob = current_image_blob  # Mantener la imagen actual si no se proporciona una nueva

                    # Actualiza los datos del inventario existente
                    cur.execute(
                        """
                    UPDATE inventory 
                    SET name = ?, category = ?, stock = ?, purchase_price = ?, sale_price = ?, totalpurch = ?, description = ?, image = ?
                    WHERE id = ?;
                    """,
                        (
                            name,
                            category,
                            stock,
                            purchase_price,
                            sale_price,
                            totalpurch,
                            description,
                            image_blob,
                            uid,
                        ),
                    )

                    conn.commit()
                    show_message(
                        "Información", "Actualización realizada en la base de datos."
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
                    cur.execute("DELETE FROM inventory WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
