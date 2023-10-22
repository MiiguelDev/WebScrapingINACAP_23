import requests
from bs4 import BeautifulSoup
import re

def obtener_precio_supermercado(url, supermercado, selector):
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

                return {"Supermercado": supermercado, "Precio": precio_limpio, "URL": url}
            else:
                return None  # No se encontró el precio en la página
        else:
            return None  # Error al obtener la página
    except Exception as e:
        return None  # Manejo de errores

def scrap_tallarines():
    resultados = []

    supermercados = ["Dipy", "Jumbo", "Distribuidora Castillo"]

    urls = [
        "https://dipy.cl/products/fideo-spaguetti-5-400grs-luchetti?variant=40524100206800&currency=CLP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic",
        "https://www.jumbo.cl/spaghetti-n-5-carozzi-bolsa-400-g-2/p",
        "https://distribuidoraelcastillo.cl/products/spaguetti-carozzi-n5-400g",
    ]

    selectores = [
        "p.sub_embalaje b",
        "span.prices-main-price#scraping-tmp",
        "span.price-item.price-item--regular"    
    ]

    for i in range(len(supermercados)):
        resultado = obtener_precio_supermercado(urls[i], supermercados[i], selectores[i])
        if resultado:
            resultados.append(resultado)

    # Encontramos el valor más bajo
    precio_mas_bajo = min(resultados, key=lambda x: float(x["Precio"].replace("$", "").replace(".", "").replace(" CLP", "")))

    return precio_mas_bajo

if __name__== "__main__":
    resultado = scrap_tallarines()
    print("Supermercado:", resultado["Supermercado"])
    print("Precio más bajo:", resultado["Precio"])
    print("URL del producto:", resultado["URL"])