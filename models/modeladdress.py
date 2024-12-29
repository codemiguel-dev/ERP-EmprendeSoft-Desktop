import sqlite3

import bcrypt
from geopy.geocoders import Nominatim
from passlib.hash import bcrypt as passlib_bcrypt

from configuration.configuration_message import show_message
from models.connect import connect_to_database


class ModelAddress:

    def register(self, country=None, region=None, commune=None, description=None):

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

                    # Inicializa los valores y parámetros para la inserción
                    insert_fields = []
                    params = []

                    if country is not None:
                        insert_fields.append("country")
                        params.append(country)

                    if region is not None:
                        insert_fields.append("region")
                        params.append(region)
                    if commune is not None:
                        insert_fields.append("commune")
                        params.append(commune)

                    if description is not None:
                        insert_fields.append("description")
                        params.append(description)

                    # Si hay campos para insertar
                    if insert_fields:
                        placeholders = ", ".join(["?"] * len(insert_fields))
                        insert_query = f"""
                            INSERT INTO address ({', '.join(insert_fields)})
                            VALUES ({placeholders});
                        """
                        cur.execute(insert_query, params)

                        show_message("Información", "Registro exitoso.")
                    else:
                        show_message(
                            "Información", "No se proporcionaron campos para registrar."
                        )

            except sqlite3.Error as e:
                show_message("Error", f"No se pudo registrar el producto: {e}")
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
