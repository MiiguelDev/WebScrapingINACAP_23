# En este codigo se incluyen las consultas para 
# 1.- Comprobar la conexion a la bd
# 2.- Comprobar los registros en la bd
# 3.- Comprobar la estructura de las tablas en la bd

import mysql.connector
from mysql.connector import Error

def create_db_connection(host, database, user, password):
    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except Error as e:
        print("Error al conectar con MySQL:", e)
        return None

def test_database_connection(host, database, user, password):
    connection = create_db_connection(host, database, user, password)
    if connection and connection.is_connected():
        connection.close()
        return "Conexion exitosa con la base de datos."
    return False

print(test_database_connection('3.22.156.122', 'comparacion_precios', 'scrapy', 'Inacap2023#'))

def fetch_all_data(host, database, user, password):
    connection = create_db_connection(host, database, user, password)
    if connection:
        try:
            cursor = connection.cursor()

            # Diccionario de consultas para cada tabla
            queries = {
                "historial_precios": """
                SELECT producto.producto_id, producto.producto_nombre, supermercado.super_nombre, historial_precios.precio, historial_precios.fecha_hora
                FROM historial_precios
                JOIN supermercado ON historial_precios.super_id = supermercado.super_id
                JOIN producto ON historial_precios.producto_id = producto.producto_id
                ORDER BY historial_precios.fecha_hora DESC
                """,
                "supermercado": "SELECT * FROM supermercado",
                "producto": "SELECT * FROM producto",
            }

            # Ejecutar todas las consultas y manejar los resultados
            for table_name, query in queries.items():
                cursor.execute(query)
                records = cursor.fetchall()

                if records:
                    print(f"\nDatos de {table_name}:")
                    for record in records:
                        if table_name == "historial_precios":
                            # Formato específico para historial_precios
                            producto_id, producto_nombre, super_nombre, precio, fecha_hora = record
                            fecha_formateada = fecha_hora.strftime("%d-%m-%Y - %H:%M:%S")
                            print(f"{producto_id:<30}{producto_nombre:<30}{super_nombre:<30}{precio:<30}{fecha_formateada}")
                        else:
                            # Formato genérico para las demás tablas
                            print(" ".join(str(r).ljust(10) for r in record))
                else:
                    print(f"No se encontraron registros en la tabla '{table_name}'.")

        except Error as e:
            print("Error al realizar la consulta:", e)
        finally:
            cursor.close()
            connection.close()

# Reemplazar con tus propios detalles de conexión
fetch_all_data('3.22.156.122', 'comparacion_precios', 'scrapy', 'Inacap2023#')


def describe_all_tables_structure(host, database, user, password):
    connection = create_db_connection(host, database, user, password)
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            for (table_name,) in tables:
                print(f"\nEstructura de la tabla {table_name}:")
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                for column in columns:
                    print(column)
        except Error as e:
            print("Error al realizar la consulta:", e)
        finally:
            cursor.close()
            connection.close()

describe_all_tables_structure('3.22.156.122', 'comparacion_precios', 'scrapy', 'Inacap2023#')
