import os
from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database


class ModelSent:

    def register(self, address, method, description, budget, status):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Inserta el cliente en la base de datos
                    cur.execute(
                        "INSERT INTO sent(address_id, method, description, price, status) VALUES (?, ?, ?, ?, ?);",
                        (address, method, description, budget, status),
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
        cursor.execute(
            """
            SELECT 
                sent.id, 
                sent.method, 
                sent.description, 
                sent.price, 
                sent.status, 
                address.country,
                address.region,        
                address.commune, 
                address.description    
            FROM sent
            INNER JOIN address ON sent.address_id = address.id;
        """
        )
        trans = cursor.fetchall()
        conn.close()

        return trans

    def update(self, uid, address, method, description, price_send, status):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Actualiza los datos del inventario existente

                    cur.execute(
                        """
                    UPDATE sent
                    SET address_id = ?, method = ?, description = ?, price = ?, status = ?
                    WHERE id = ?;
                    """,
                        (address, method, description, price_send, status, uid),
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
                    cur.execute("DELETE FROM sent WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
