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
# Asegúrate de que los IDs de los nuevos productos continúen la secuencia de los ya existentes.
productos = [
    (1, 'Aceite'),
    (2, 'Azucar'),
    (3, 'Atun'),
    (4, 'Lavalozas'),
    (5, 'Agua'),
    (6, 'Te'),
    (7, 'Mantequilla'),
    (8, 'Leche'),
    (9, 'Lenteja'),
    (10, 'Salchichas')
]

insert_producto_query = "INSERT INTO producto (producto_id, producto_nombre) VALUES (%s, %s)"
cursor.executemany(insert_producto_query, productos)
conexion.commit()

# Insertar registros en la tabla historial_precios para los nuevos productos
# Asegúrate de actualizar el número total de productos y supermercados si estos cambian.
insert_historial_precios_query = """
INSERT INTO historial_precios (super_id, producto_id, precio, fecha_hora)
SELECT s.super_id, p.producto_id, 1000 + (s.super_id * 10) + p.producto_id, NOW()
FROM (SELECT super_id FROM supermercado) s
CROSS JOIN (SELECT producto_id FROM producto) p
"""

cursor.execute(insert_historial_precios_query)
conexion.commit()

# Cerrar la conexión y el cursor
cursor.close()
conexion.close()

