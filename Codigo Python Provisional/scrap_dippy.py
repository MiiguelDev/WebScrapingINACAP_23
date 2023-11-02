import requests
from bs4 import BeautifulSoup
import re

def scrap_product_info(supermercados, producto, urls, selectores):
    resultados = []

    for i in range(len(supermercados)):
        supermercado = supermercados[i]
        url = urls[i]
        selector = selectores[i]

        try:
            # Realizamos una solicitud GET para obtener el contenido de la página
            response = requests.get(url)

            # Verificamos si la solicitud fue exitosa (código de respuesta 200)
            if response.status_code == 200:
                # Parseamos el contenido HTML de la página usando BeautifulSoup
                soup = BeautifulSoup(response.content, "html.parser")

                # Utilizamos select_one para encontrar el elemento que contiene el precio
                precio_element = soup.select_one(selector)

                if precio_element:
                    # Extraemos el texto del elemento que contiene el precio
                    precio_text = precio_element.text.strip()

                    # Utilizamos una expresión regular para extraer solo los dígitos y el punto decimal
                    precio_limpio = re.sub(r'[^\d.]', '', precio_text)

                    resultado = {"Supermercado": supermercado, "Precio": precio_limpio, "URL": url}
                    resultados.append(resultado)

        except Exception as e:
            print("Error en la solicitud:", e)

    return resultados

# Ejemplo de uso
supermercados = ["Dipy"]
producto = "Parma Fideo Spaghetti N° 5 400 Gr"
urls = ["https://dipy.cl/collections/fideos-pastas-y-salsa/products/fideo-spaghetti-n-5-400-gr"]
selectores = ['.price-list span[style="color:gray; font-size:12px"]']

resultados = scrap_product_info(supermercados, producto, urls, selectores)

if resultados:
    for resultado in resultados:
        print("Supermercado:", resultado["Supermercado"])
        print("Precio:", resultado["Precio"])
        print("URL:", resultado["URL"])
else:
    print("No se encontro info.")



