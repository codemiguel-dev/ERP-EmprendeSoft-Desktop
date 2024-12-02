import sqlite3
from configuration.configuration_message import show_message


from models.connect import connect_to_database


class ModelProject:

    def register(self, name, description, budget, status, type_project):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Inserta el nuevo usuario en la base de datos con la imagen como BLOB
                    cur.execute(
                        """
                        INSERT INTO project (name, description, budget, status, type_project) 
                        VALUES (?, ?, ?, ?, ?);
                        """,
                        (name, description, budget, status, type_project),
                    )

                show_message("Información", "Registro exitoso.")
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM project")
        project = cursor.fetchall()
        conn.close()

        return project

    def update(self, uid, name, description, budget, status, type_project):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Actualiza los datos del inventario existente
                    cur.execute(
                        """
                    UPDATE project 
                    SET name = ?, description = ?, budget = ?, status = ?, type_project = ?
                    WHERE id = ?;
                    """,
                        (
                            name,
                            description,
                            budget,
                            status,
                            type_project,
                            uid,
                        ),
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
                    cur.execute("DELETE FROM project WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
