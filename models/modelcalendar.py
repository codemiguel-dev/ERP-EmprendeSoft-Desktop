import os
from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database


class ModelCalendar:

    def register(self, employee, start_time, end_time, horary):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Inserta el cliente en la base de datos
                    cur.execute(
                        "INSERT INTO calendar (employee_id, start_time, end_time, horary) VALUES (?, ?, ?, ?);",
                        (employee, start_time, end_time, horary),
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
        SELECT user.name, employee.job, calendar.id, calendar.start_time, calendar.end_time, calendar.horary
        FROM employee 
        INNER JOIN calendar
        ON employee.id = calendar.employee_id
        INNER JOIN user
        ON employee.user_id = user.id;
        """
        cursor.execute(query)
        horary = cursor.fetchall()
        conn.close()

        return horary

    def update(self, uid, employee, start_time, end_time, horary):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Actualiza los datos del inventario existente
                    cur.execute(
                        """
                    UPDATE calendar
                    SET employee_id = ?, start_time = ?, end_time = ?, horary = ?
                    WHERE id = ?;
                    """,
                        (
                            employee,
                            start_time,
                            end_time,
                            horary,
                            uid,
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
                    cur.execute("DELETE FROM calendar WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
