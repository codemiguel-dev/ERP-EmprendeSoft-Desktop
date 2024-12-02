import sqlite3
from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database
from view.standar.viewdashboard import Viewdashboardstandar


class ModelTransaction:

    def register(self, id_transaction, amount, type_transaction, entity, type_pay):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Verifica si el usuario ya existe
                    cur.execute(
                        "SELECT * FROM transactions WHERE transaction_id = ?",
                        (id_transaction,),
                    )
                    user_data = cur.fetchone()

                    if user_data:
                        show_message("Error", "La transaction ya existe.")
                    else:

                        # Inserta el nuevo usuario en la base de datos con la imagen como BLOB
                        cur.execute(
                            """
                        INSERT INTO transactions (transaction_id, amount, transaction_type, entity, payment_type) 
                        VALUES ( ?, ?, ?, ?, ?);
                        """,
                            (
                                id_transaction,
                                amount,
                                type_transaction,
                                entity,
                                type_pay,
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
        cursor.execute("SELECT * FROM transactions")
        inventory = cursor.fetchall()
        conn.close()

        return inventory

    def update(self, uid, date, amount, type_transaction, entity, type_payment):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute(
                        """
                    UPDATE transactions 
                    SET transaction_date = ?, amount = ?, transaction_type = ?, entity = ?, payment_type = ?
                    WHERE id = ?;
                    """,
                        (date, amount, type_transaction, entity, type_payment, uid),
                    )

                    conn.commit()
                    show_message(
                        "Información", "Actualización realizada en la base de datos."
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
                    cur.execute("DELETE FROM transactions WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get_transaction_graph(self):
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()

                # Consulta SQL corregida
                query = """
                SELECT transaction_date, amount FROM transactions
                """

                cursor.execute(query)
                transaction = cursor.fetchall()

            finally:
                conn.close()

            return transaction
        else:
            print("No se pudo conectar a la base de datos.")
            return None
