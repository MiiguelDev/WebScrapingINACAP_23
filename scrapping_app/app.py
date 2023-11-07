from flask import Flask, render_template
from selenium_ejemplo import scrap_product_info
from data_scrapping import data;
import json

app = Flask(__name__)

# Definimos la pagina de inicio "/" indica que es la raiz del proyecto.
@app.route('/')
def home():
    return render_template('home.html')

# Definimos un apartado en que muestra los datos de scrapping en formato json.
# Esto es con solo fines practicos, se puede quitar luego.
@app.route('/data')
def data_dicts():
    data_json = json.dumps(data, indent=4) 
    return render_template('data.html', data_json=data_json)


@app.route('/aceite')
def mostrar_precio_aceite():
    categoria = "Aceite"  # Reemplaza con la categoría que corresponda
    supermercados = data[categoria]  # Obtiene los datos de los supermercados para la categoría extrayendolos del modulo "data.scrapping.py"

    resultados = []

    for supermercado, datos_supermercado in supermercados.items():
        producto = categoria
        url = datos_supermercado['Link']
        selector = datos_supermercado['Selector']
        imagen_producto = datos_supermercado['Imagenes']

        resultado = scrap_product_info([supermercado], [producto], [url], [selector], [imagen_producto])

        if resultado:
            resultados.extend(resultado)

    if resultados:
        # Ordena la lista de resultados por el precio (de menor a mayor)
        resultados = sorted(resultados, key=lambda x: x['Precio'])

        if resultados:
            # Ahora, resultados[0] contiene el precio mas bajo y lo recuperamos
            # en una variable extra para aislarlo en el hmtl
            resultado_mas_bajo = resultados[0]

            return render_template('precio_aceite.html', resultados=resultados, resultado_mas_bajo=resultado_mas_bajo)
    return "No se encontraron resultados"



if __name__ == "__main__":
    app.run(debug=True)
