# Description: Este script se encarga de limpiar todas las tablas de la base de datos.

import mysql.connector
from mysql.connector import Error

def truncate_all_tables(host, database, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        # Desactivar las restricciones de clave foránea
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Obtener una lista de todas las tablas en la base de datos
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for (table_name,) in tables:
            print(f"Truncando tabla {table_name}...")
            cursor.execute(f"TRUNCATE TABLE {table_name}")

        # Reactivar las restricciones de clave foránea
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        connection.commit()
        print("Todas las tablas han sido truncadas con éxito.")

    except Error as e:
        print("Error al conectar con MySQL:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

truncate_all_tables('3.22.156.122', 'comparacion_precios', 'scrapy', 'Inacap2023#')

