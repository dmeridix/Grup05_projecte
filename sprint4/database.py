import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia según tu configuración
        password="Reyney15",  # Cambia según tu configuración
        database="proyecto",
        charset='utf8mb4',  # Cambiar el conjunto de caracteres
        collation='utf8mb4_general_ci'  # Opcional, dependiendo del cliente
    )
