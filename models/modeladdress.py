import sqlite3

import bcrypt
from geopy.geocoders import Nominatim
from passlib.hash import bcrypt as passlib_bcrypt

from configuration.configuration_message import show_message
from models.connect import connect_to_database


class ModelAddress:

    def register(self, country, region, commune, description):

        # Crear una dirección completa para buscar las coordenadas
        full_address = f"{description}, {commune}, {region}, {country}"

        # Utilizar geopy para obtener las coordenadas
        geolocator = Nominatim(user_agent="mi_aplicacion_geocodificador")
        location = geolocator.geocode(full_address)

        if location is None:
            show_message(
                "Error", "No se pudieron obtener las coordenadas de la dirección."
            )
            return

        latitude = location.latitude
        longitude = location.longitude

        # Conectar a la base de datos
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Inserta la nueva dirección en la tabla address
                    cur.execute(
                        """
                        INSERT INTO address (country, region, commune, description) 
                        VALUES (?, ?, ?, ?);
                        """,
                        (country, region, commune, description),
                    )

                    show_message("Información", "Información registrada.")
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")

    def get(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM address")
        address = cursor.fetchall()
        conn.close()

        return address

    def update(self, uid, region, commune, address):
        conn = connect_to_database()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()

                    # Actualiza los datos del inventario existente
                    cur.execute(
                        """
                    UPDATE address
                    SET region = ?, commune = ?, description = ?
                    WHERE id = ?;
                    """,
                        (region, commune, address, uid),
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
                    cur.execute("DELETE FROM inventory WHERE id = ?;", (uid,))
                    show_message(
                        "Información", "Eliminación realizada en la base de datos."
                    )
            finally:
                conn.close()
        else:
            show_message("Error", "No se pudo conectar a la base de datos.")
