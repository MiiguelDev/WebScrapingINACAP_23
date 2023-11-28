import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        return connection
    except Error as err:
        print(f"Error: '{err}'")
        return None

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        cursor.close()

def truncate_all_tables(connection):
    try:
        # Desactivar las restricciones de clave foránea
        execute_query(connection, "SET FOREIGN_KEY_CHECKS = 0")

        # Obtener una lista de todas las tablas en la base de datos
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for (table_name,) in tables:
            print(f"Truncando tabla {table_name}...")
            execute_query(connection, f"TRUNCATE TABLE {table_name}")

        # Reactivar las restricciones de clave foránea
        execute_query(connection, "SET FOREIGN_KEY_CHECKS = 1")

        print("Todas las tablas han sido truncadas con éxito.")

    except Error as err:
        print(f"Error: '{err}'")
    finally:
        cursor.close()

def main():
    host = '3.22.156.122'
    database = 'comparacion_precios'
    user = 'scrapy'
    password = 'Inacap2023#'

    connection = create_db_connection(host, user, password, database)
    if connection is not None:
        truncate_all_tables(connection)
        connection.close()

if __name__ == "__main__":
    main()


