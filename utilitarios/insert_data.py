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

def execute_query(connection, query, data=None):
    try:
        cursor = connection.cursor()
        if data:
            cursor.executemany(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        cursor.close()
    except Error as err:
        print(f"Error: '{err}'")

def main():
    # Detalles de la conexión
    host = "3.22.156.122"
    user = "scrapy"
    password = "Inacap2023#"
    database = "comparacion_precios"

    # Crear conexión a la base de datos
    connection = create_db_connection(host, user, password, database)
    if connection is None:
        return

    # Insertar registros de supermercados
    insert_supermercado_query = "INSERT INTO supermercado (super_id, super_nombre) VALUES (%s, %s)"
    supermercados = [(1, 'Lider'), (2, 'Jumbo'), (3, 'Santa Isabel'), (4, 'Cugat')]
    execute_query(connection, insert_supermercado_query, supermercados)

    # Insertar registros de productos
    insert_producto_query = "INSERT INTO producto (producto_id, producto_nombre) VALUES (%s, %s)"
    productos = [(i, nombre) for i, nombre in enumerate(['Aceite', 'Azucar', 'Atun', 'Lavalozas', 'Agua', 'Te', 'Mantequilla', 'Leche', 'Lenteja', 'Salchichas'], start=1)]
    execute_query(connection, insert_producto_query, productos)

    # Insertar registros en historial_precios
    insert_historial_precios_query = """
    INSERT INTO historial_precios (super_id, producto_id, precio, fecha_hora)
    SELECT s.super_id, p.producto_id, 1000 + (s.super_id * 10) + p.producto_id, NOW()
    FROM (SELECT super_id FROM supermercado) s
    CROSS JOIN (SELECT producto_id FROM producto) p
    """
    execute_query(connection, insert_historial_precios_query)

    # Cerrar la conexión
    connection.close()

if __name__ == "__main__":
    main()


