# Este script inserta datos de prueba en la base de datos comparacion_precios

import mysql.connector

# Establecer la conexión con la base de datos
conexion = mysql.connector.connect(
    host="3.22.156.122",
    user="scrapy",
    password="Inacap2023#",
    database="comparacion_precios"
)

# Crear el cursor para ejecutar las consultas
cursor = conexion.cursor()

# Insertar registros de supermercados con números correlativos
supermercados = [
    (1, 'Lider'),
    (2, 'Jumbo'),
    (3, 'Santa Isabel'),
    (4, 'Cugat')
]

insert_supermercado_query = "INSERT INTO supermercado (super_id, super_nombre) VALUES (%s, %s)"
cursor.executemany(insert_supermercado_query, supermercados)
conexion.commit()

# Insertar registros de productos con números correlativos
productos = [
    (1, 'Aceite'),
    (2, 'Azucar'),
    (3, 'Atun'),
    (4, 'Lavalozas'),
    (5, 'Agua')
]

insert_producto_query = "INSERT INTO producto (producto_id, producto_nombre) VALUES (%s, %s)"
cursor.executemany(insert_producto_query, productos)
conexion.commit()

# Insertar 30 filas adicionales en la tabla historial_precios
insert_historial_precios_query = """
INSERT INTO historial_precios (historial_id, super_id, producto_id, precio, fecha_hora)
SELECT (i % 30) + 1, (i % 4) + 1, (i % 5) + 1, 1000 + (i - 1) * 10, DATE_ADD('2023-11-01 08:00:00', INTERVAL (i - 1) HOUR)
FROM (
  SELECT (t4.a + t5.a * 4 + 1) AS i
  FROM (SELECT 0 AS a UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) AS t4
  CROSS JOIN (SELECT 0 AS a UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) AS t5
) AS numbers
"""

cursor.execute(insert_historial_precios_query)
conexion.commit()

# Cerrar la conexión y el cursor
cursor.close()
conexion.close()
