import os

import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from configuration.configuration_message import show_message
from models.connect import connect_to_database


class ModelInvestment:

    def register(self, types, amount, amount_end, yields, date):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Inserta el cliente en la base de datos
                    cur.execute(
                        "INSERT INTO investment (type, amount, amount_end, yield, expiration_date) VALUES (?, ?, ?, ?, ?);",
                        (types, amount, amount_end, yields, date),
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
        cursor.execute("SELECT * FROM investment")
        inv = cursor.fetchall()
        conn.close()

        return inv

    def get_graphi(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT date, amount, amount_end, yield FROM investment;")
        inv = cursor.fetchall()
        conn.close()

        return inv

    def update(self, uid, types, amount, amount_end, yields, date_expiration):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Actualiza los datos del inventario existente

                    cur.execute(
                        """
                    UPDATE investment
                    SET type = ?, amount = ?, amount_end = ?, yield = ?, expiration_date = ?
                    WHERE id = ?;
                    """,
                        (types, amount, amount_end, yields, date_expiration, uid),
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
                    cur.execute("DELETE FROM investment WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
