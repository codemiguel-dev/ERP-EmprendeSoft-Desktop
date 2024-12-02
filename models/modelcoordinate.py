import os
from configuration.configuration_message import show_message


import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt

from models.connect import connect_to_database


class ModelCoordinate:

    def get(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM coordinate")
        coordinate = cursor.fetchall()
        conn.close()

        return coordinate

    def register(self, address_id, uuid, lat, lon):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    # Verifica si el cliente ya existe
                    # cur.execute("SELECT * FROM client WHERE name = ?", (name,))
                    # user_data = cur.fetchone()
                    # if user_data:
                    #    messagebox.showerror("Error", "El cliente ya existe.")
                    # else:

                    # Inserta el cliente en la base de datos
                    cur.execute(
                        "INSERT INTO coordinate (address_id, uuid, lat, lon) VALUES (?, ?, ?, ?);",
                        (address_id, uuid, lat, lon),
                    )

                    show_message("Información", "Registro exitoso.")
                    # Opcional: abrir la ventana principal
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
