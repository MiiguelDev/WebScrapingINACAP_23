from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = '3.22.156.122'
app.config['MYSQL_USER'] = 'scrapy'
app.config['MYSQL_PASSWORD'] = 'Inacap2023#'
app.config['MYSQL_DB'] = 'comparacion_precios'

mysql = MySQL(app)

@app.route('/')
def index():
    producto_ids = [1,2,3,4,5]  # Lista de IDs de productos, 
                                # para agregar otro producto solo se debe agregar su ID a esta lista
    results = {}  # Diccionario para almacenar los datos de cada producto

    for i, producto_id in enumerate(producto_ids, start=1):
        cur = mysql.connection.cursor()
        cur.execute("""
        SELECT s.super_nombre, p.producto_nombre, hp.precio
        FROM historial_precios hp
        INNER JOIN (
            SELECT super_id, producto_id, MAX(fecha_hora) AS fecha_maxima
            FROM historial_precios
            WHERE producto_id = %s
            GROUP BY super_id, producto_id
        ) AS ultimos_precios ON hp.super_id = ultimos_precios.super_id AND hp.producto_id = ultimos_precios.producto_id AND hp.fecha_hora = ultimos_precios.fecha_maxima
        JOIN supermercado s ON hp.super_id = s.super_id
        JOIN producto p ON hp.producto_id = p.producto_id
        ORDER BY hp.precio ASC LIMIT 1
        """, (producto_id,))
        results[f'product{i}_data'] = cur.fetchall()
        cur.close()

    # Desempaquetar el diccionario 'results' para pasar cada conjunto de datos de productos individualmente
    return render_template('index.html', 
                           product1_data=results.get('product1_data', []), 
                           product2_data=results.get('product2_data', []), 
                           product3_data=results.get('product3_data', []), 
                           product4_data=results.get('product4_data', []), 
                           product5_data=results.get('product5_data', []))
                        # Luego de agregar otro producto, se debe agregar una nueva variable 
                        # para pasar los datos de ese producto (ej: product6_data, product7_data, etc.)
                        

@app.route('/aceite')
def aceite():
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT s.super_nombre, p.producto_nombre, hp.precio, hp.fecha_hora
    FROM historial_precios hp
    INNER JOIN (
        SELECT super_id, MAX(fecha_hora) AS fecha_maxima
        FROM historial_precios
        JOIN producto ON producto.producto_id = historial_precios.producto_id
        WHERE producto.producto_nombre = 'Aceite'
        GROUP BY super_id
    ) AS ultimos_precios ON hp.super_id = ultimos_precios.super_id AND hp.fecha_hora = ultimos_precios.fecha_maxima
    JOIN supermercado s ON hp.super_id = s.super_id
    JOIN producto p ON hp.producto_id = p.producto_id
    WHERE p.producto_nombre = 'Aceite'
    ORDER BY hp.precio ASC
    """)
    aceite_data = cur.fetchall()
    cur.close()

    return render_template('precio_aceite.html', aceite_data=aceite_data)



if __name__ == '__main__':
    app.run(debug=True)



