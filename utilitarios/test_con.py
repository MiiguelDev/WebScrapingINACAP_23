import mysql.connector
from mysql.connector import Error

# Crear conexión a la base de datos
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

# Comprobar la conexión a la base de datos
def test_database_connection(connection):
    if connection and connection.is_connected():
        return "Conexion exitosa con la base de datos."
    return False

# Ejecutar una consulta SQL y obtener los resultados
def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print("Error al realizar la consulta:", e)
    finally:
        cursor.close()

# Fetch all data from all tables
def fetch_all_data(connection):
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

    for table_name, query in queries.items():
        records = execute_query(connection, query)
        if records:
            print(f"\nDatos de {table_name}:")
            for record in records:
                print_record(table_name, record)
        else:
            print(f"No se encontraron registros en la tabla '{table_name}'.")

# Print records with specific formatting
def print_record(table_name, record):
    if table_name == "historial_precios":
        producto_id, producto_nombre, super_nombre, precio, fecha_hora = record
        fecha_formateada = fecha_hora.strftime("%d-%m-%Y - %H:%M:%S")
        print(f"{producto_id:<30}{producto_nombre:<30}{super_nombre:<30}{precio:<30}{fecha_formateada}")
    else:
        print(" ".join(str(r).ljust(10) for r in record))

# Describe the structure of all tables
def describe_all_tables_structure(connection):
    tables = execute_query(connection, "SHOW TABLES")
    for (table_name,) in tables:
        print(f"\nEstructura de la tabla {table_name}:")
        columns = execute_query(connection, f"DESCRIBE {table_name}")
        for column in columns:
            print(column)

# Main execution
if __name__ == "__main__":
    host = '3.22.156.122'
    database = 'comparacion_precios'
    user = 'scrapy'
    password = 'Inacap2023#'

    connection = create_db_connection(host, database, user, password)
    
    # Test Database Connection
    print(test_database_connection(connection))

    # Fetch and print all data from tables
    if connection.is_connected():
        fetch_all_data(connection)
    
    # Describe all tables
    if connection.is_connected():
        describe_all_tables_structure(connection)

    if connection.is_connected():
        connection.close()

