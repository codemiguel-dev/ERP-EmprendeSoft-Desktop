import os
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
        name=None,
        category=None,
        stock=None,
        purchase_price=None,
        sale_price=None,
        totalpurch=None,
        description=None,
        image_path=None,
    ):
        """
        Actualiza un registro en la tabla 'inventory' de forma dinámica.

        :param uid: ID del registro a actualizar.
        :param name: Nuevo nombre del producto (opcional).
        :param category: Nueva categoría del producto (opcional).
        :param stock: Nuevo stock del producto (opcional).
        :param purchase_price: Nuevo precio de compra del producto (opcional).
        :param sale_price: Nuevo precio de venta del producto (opcional).
        :param totalpurch: Nuevo total de compras del producto (opcional).
        :param description: Nueva descripción del producto (opcional).
        :param image_path: Ruta de la nueva imagen del producto (opcional).
        """
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Inicializa los valores a actualizar y los parámetros
                    update_fields = []
                    params = []

                    # Agrega los campos dinámicamente
                    if name is not None:
                        update_fields.append("name = ?")
                        params.append(name)

                    if category is not None:
                        update_fields.append("category = ?")
                        params.append(category)

                    if stock is not None:
                        update_fields.append("stock = ?")
                        params.append(stock)

                    if purchase_price is not None:
                        update_fields.append("purchase_price = ?")
                        params.append(purchase_price)

                    if sale_price is not None:
                        update_fields.append("sale_price = ?")
                        params.append(sale_price)

                    if totalpurch is not None:
                        update_fields.append("totalpurch = ?")
                        params.append(totalpurch)

                    if description is not None:
                        update_fields.append("description = ?")
                        params.append(description)

                    if image_path:
                        try:
                            # Verifica que la imagen sea una ruta válida
                            if not os.path.isfile(image_path):
                                raise FileNotFoundError(
                                    "La imagen seleccionada no se encontró."
                                )
                            with open(image_path, "rb") as file:
                                image_data = sqlite3.Binary(file.read())
                            update_fields.append("image = ?")
                            params.append(image_data)
                        except FileNotFoundError:
                            show_message(
                                "Error", "La imagen seleccionada no se encontró."
                            )
                            return

                    # Solo procede si hay campos para actualizar
                    if update_fields:
                        update_query = f"""
                            UPDATE inventory 
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
                    cur.execute("DELETE FROM inventory WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
