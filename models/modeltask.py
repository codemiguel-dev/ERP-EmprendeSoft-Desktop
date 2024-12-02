import os
from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database


class ModelTask:

    def register(self, user_id, name, description, status):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Inserta el cliente en la base de datos
                    cur.execute(
                        "INSERT INTO task (user_id, name, description, status) VALUES (?, ?, ?, ?);",
                        (user_id, name, description, status),
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
            user.id AS user_id,
            user.name AS user_name,
            task.id AS task_id,
            task.name AS task_name,
            task.description AS task_description,
            task.status AS task_status
        FROM 
            user
        INNER JOIN 
            task
        ON 
            user.id = task.user_id;
        """

        cursor.execute(query)
        task = cursor.fetchall()
        conn.close()

        return task

    def update(self, id_task, user_id, name, description, status):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Actualiza los datos del inventario existente
                    print(id_task)

                    cur.execute(
                        """
                    UPDATE task
                    SET user_id = ?, name = ?, description = ?, status = ?
                    WHERE id = ?;
                    """,
                        (
                            user_id,
                            name,
                            description,
                            status,
                            id_task,
                        ),
                    )

                    show_message(
                        "Información", "Actualización realizada en la base de datos."
                    )
                    return conn.commit()

            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def delete(self, id_task):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Elimina el registro del inventario existente
                    cur.execute("DELETE FROM task WHERE id = ?;", (id_task,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
