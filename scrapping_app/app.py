from flask import Flask, render_template
from selenium_ejemplo import scrap_product_info

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tallarines')
def mostrar_precio_tallarines():
    supermercados = ["Lider"]
    producto = "Fideo Spaghetti N° 5 400 Gr"
    urls = ["https://www.lider.cl/supermercado/product/sku/576170/Lider-Spaghetti-5"]
    selectores = ['pdp-mobile-sales-price']
    imagen_producto = ['https://dipy.cl/cdn/shop/products/cl_z108025_500x.jpg?v=1661811374']
    
    resultados = scrap_product_info(supermercados, producto, urls, selectores, imagen_producto)
    
    if resultados:  # Comprueba si la lista de resultados no esta vacia
        return render_template('precio_tallarines.html', resultados=resultados)
    else:
        # Manejar el caso en que no se obtuvieron resultados
        return "No se encontraron resultados"


if __name__ == "__main__":
    app.run(debug=True)
