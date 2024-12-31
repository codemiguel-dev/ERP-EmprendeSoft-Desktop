import os
import sqlite3

import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from configuration.configuration_message import show_message
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

                    # Inicializa los valores a actualizar y los parámetros
                    update_fields = []
                    params = []

                    # Agrega los campos dinámicamente
                    if employee is not None:
                        update_fields.append("employee_id = ?")
                        params.append(employee)

                    # Agrega los campos dinámicamente
                    if start_time is not None:
                        update_fields.append("start_time = ?")
                        params.append(start_time)

                    # Agrega los campos dinámicamente
                    if end_time is not None:
                        update_fields.append("end_time = ?")
                        params.append(end_time)

                    # Agrega los campos dinámicamente
                    if horary is not None:
                        update_fields.append("horary = ?")
                        params.append(horary)

                    # Solo procede si hay campos para actualizar
                    if update_fields:
                        update_query = f"""
                            UPDATE calendar 
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
                    cur.execute("DELETE FROM calendar WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
