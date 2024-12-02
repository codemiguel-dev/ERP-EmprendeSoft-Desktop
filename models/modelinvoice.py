import sqlite3

import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from configuration.configuration_message import show_message
from models.connect import connect_to_database
from view.standar.viewdashboard import Viewdashboardstandar


class ModelInvoice:

    def register(self, user, client, total, code):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Inserta el nuevo usuario en la base de datos con la imagen como BLOB
                    cur.execute(
                        """
                        INSERT INTO invoice (client_id, user_id, total, code) 
                        VALUES (?, ?, ?, ?);
                    """,
                        (client, user, total, code),
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

    def register_item(self, product_id, product_quantity, product_total, code):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Obtener el ID de la factura
                    cur.execute(
                        """
                    SELECT id 
                    FROM invoice 
                    WHERE code = ?;
                    """,
                        (code,),
                    )

                    # Obtener el resultado
                    invoice_id = cur.fetchone()
                    if invoice_id:
                        invoice_id = invoice_id[0]  # invoice_id es una tupla
                        print("ID de la factura:", invoice_id)

                        # Obtener el stock actual y el precio unitario del producto desde la tabla de inventario
                        cur.execute(
                            """
                        SELECT stock, sale_price
                        FROM inventory
                        WHERE id = ?;
                        """,
                            (product_id,),
                        )

                        product_data = cur.fetchone()
                        if product_data:
                            current_stock, sale_price = product_data
                            print("Stock actual:", current_stock)
                            print("Precio unitario:", sale_price)

                            # Calcular el nuevo stock
                            new_stock = current_stock - product_quantity

                            if new_stock >= 0:
                                # Actualizar el stock en la tabla de inventario
                                cur.execute(
                                    """
                                UPDATE inventory
                                SET stock = ?
                                WHERE id = ?;
                                """,
                                    (new_stock, product_id),
                                )

                                new_total_purch = new_stock * sale_price

                                cur.execute(
                                    """
                                UPDATE inventory
                                SET totalpurch = ?
                                WHERE id = ?;
                                """,
                                    (new_total_purch, product_id),
                                )

                                # Calcular el total (nuevo stock * precio unitario)
                                product_total = product_quantity * sale_price

                                # Insertar el nuevo registro del producto en la base de datos
                                cur.execute(
                                    """
                                INSERT INTO invoice_item (invoice_id, inventory_id, quantity, total_price)
                                VALUES (?, ?, ?, ?);
                                """,
                                    (
                                        invoice_id,
                                        product_id,
                                        product_quantity,
                                        product_total,
                                    ),
                                )

                                show_message(
                                    "Información",
                                    "Registro exitoso y stock actualizado.",
                                )
                            else:
                                print("No hay suficiente stock disponible.")
                                show_message("Error", "Stock insuficiente.")
                        else:
                            print("No se encontró el producto en el inventario.")
                            show_message(
                                "Error", "Producto no encontrado en el inventario."
                            )
                    else:
                        print("No se encontró la factura para el código proporcionado.")
                        show_message("Error", "Factura no encontrada.")

            except Exception as e:
                print("Ocurrió un error:", e)
                show_message("Error", "No se pudo registrar el ítem.")
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get(self):
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()

                # Consulta SQL corregida
                query = """
                SELECT
                    i.name, 
                    i.purchase_price,
                    i.sale_price,
                    ii.quantity,   
                    ii.total_price,
                    ii.id
                FROM 
                    inventory i   
                JOIN 
                    invoice_item ii      
                ON 
                    ii.inventory_id = i.id
                """

                cursor.execute(query)
                invoice = cursor.fetchall()

            finally:
                conn.close()

            return invoice
        else:
            print("No se pudo conectar a la base de datos.")

    def get_invoice_graph(self):
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()

                # Consulta SQL corregida
                query = """
                SELECT 
                    ii.total_price,   
                    i.name          
                FROM 
                    invoice_item ii  
                JOIN 
                    inventory i      
                ON 
                    ii.inventory_id = i.id
                """

                cursor.execute(query)
                invoice = cursor.fetchall()

            finally:
                conn.close()

            return invoice
        else:
            print("No se pudo conectar a la base de datos.")
            return None

    def get_user(self, id):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM user WHERE id = ?", (id,))
                    user = cur.fetchone()
                    if user:
                        return user
                    else:
                        print("Usuario no encontrado.")
            except sqlite3.Error as e:
                print(f"Error al buscar el usuario: {e}")
            finally:
                conn.close()
        else:
            print("No se pudo conectar a la base de datos.")

    def delete(self, uid):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Elimina el registro del inventario existente
                    cur.execute("DELETE FROM invoice_item WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
