import os
import sqlite3

import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from configuration.configuration_message import show_message
from models.connect import connect_to_database


class ModelGoal:

    def register(self, business_id, name, description, status, start_date, end_date):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Inserta el nuevo usuario en la base de datos con la imagen como BLOB
                    cur.execute(
                        """
                        INSERT INTO business_goals (business_id, name, description, status, start_date, end_date) 
                        VALUES (?, ?, ?, ?, ?, ?);
                        """,
                        (business_id, name, description, status, start_date, end_date),
                    )

                show_message("Información", "Registro exitoso.")
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get(self):
        conn = connect_to_database()
        cursor = conn.cursor()

        # INNER JOIN entre business y address
        cursor.execute(
            """
        SELECT 
		    business_goals.id, 
            business_goals.name,
            business_goals.description,
            business_goals.status,
            business_goals.start_date,
            business_goals.end_date,
            business.id, 
            business.name
        FROM 
            business_goals
        INNER JOIN 
            business
        ON 
            business.id = business_goals.business_id ;
        """
        )

        business = cursor.fetchall()  # Obtener todos los resultados de la consulta
        conn.close()

        return business

    def update(self, uid, name, descripcion, start_date, end_date):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Actualiza los datos del inventario existente
                    cur.execute(
                        """
                    UPDATE business_goals 
                    SET name = ?,  description = ?, start_date = ?, end_date = ? 
                    WHERE id = ?;
                    """,
                        (
                            name,
                            descripcion,
                            start_date,
                            end_date,
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
                    cur.execute("DELETE FROM business_goals WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
