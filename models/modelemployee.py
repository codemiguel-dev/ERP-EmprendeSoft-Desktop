import os
from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database


class ModelEmployee:

    def register(self, user_id, job):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Inserta el cliente en la base de datos
                    cur.execute(
                        "INSERT INTO employee (user_id, job) VALUES (?, ?);",
                        (user_id, job),
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
        query = """
        SELECT 
            user.id,
            user.name,
            employee.id,
            employee.job
        FROM 
            user
        INNER JOIN 
            employee
        ON 
            user.id = employee.user_id;
        """
        cursor.execute(query)
        trans = cursor.fetchall()
        conn.close()

        return trans

    def update(self, uid, user_id, id_employee, job):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Actualiza los datos del inventario existente

                    cur.execute(
                        """
                    UPDATE employee
                    SET  user_id= ?, job = ?
                    WHERE id = ?;
                    """,
                        (
                            user_id,
                            job,
                            id_employee,
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
                    cur.execute("DELETE FROM employee WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
