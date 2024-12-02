import sqlite3

def connect_to_database():
    try:
        conn = sqlite3.connect("./database/store.db")
        print("Conexión exitosa a la base de datos.")
        return conn
    except sqlite3.Error as e:
        print("Error al conectarse a la base de datos:", e)
        return None
