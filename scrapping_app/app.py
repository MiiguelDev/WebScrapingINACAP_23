from flask import Flask, render_template
from flask_mysqldb import MySQL
from scrap_manual.data import DATA
from descripcion import descripciones



app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = '3.22.156.122'
app.config['MYSQL_USER'] = 'scrapy'
app.config['MYSQL_PASSWORD'] = 'Inacap2023#'
app.config['MYSQL_DB'] = 'comparacion_precios'

mysql = MySQL(app)

@app.route('/')
def index():
    producto_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    products = []

    for producto_id in producto_ids:
        cur = mysql.connection.cursor()
        cur.execute("""
        SELECT s.super_nombre, p.producto_nombre, ROUND(hp.precio) AS precio
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
        data = cur.fetchone()  # fetchone devuelve una sola fila o None si no hay datos
        cur.close()

        if data:
            supermercado, producto_nombre, precio = data
            imagen_url = DATA[producto_nombre][supermercado]['Imagenes']
            producto_link = DATA[producto_nombre][supermercado]['Link']
            descripcion = descripciones.get(producto_nombre, 'Descripción no disponible.')

            products.append({
                'supermercado': supermercado,
                'nombre': producto_nombre,
                'precio': precio,
                'imagen': imagen_url,
                'link': producto_link,
                'descripcion': descripcion,
            })
        else:
            products.append({})

    return render_template('index.html', products=products)

                        

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



