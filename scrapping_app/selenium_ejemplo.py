import selenium
import re
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid  # Importa la biblioteca uuid para generar identificadores unicos

# Primero instalamos Selenium usando "pip install selenium", luego debemos encontrar la version de Chrome que tenemos instalada
# En este caso la Versión 118.0.5993.118 que es la mas actualizada. Luego debemos buscar la version de 
# ChromeDriver compatible, en este caso la pueden encontrar en https://googlechromelabs.github.io/chrome-for-testing/#stable 
# Ojo, esta version solo sirve para la version 118. de Chrome. Deben colocar el .exe que esta en la carpeta comprimida en
# el directorio raiz que es la ruta por defecto donde busca ChromeDriver para ejecutarse.

def scrap_product_info(supermercados, producto, urls, selectores, imagenes):
    resultados = []

    # Inicializa el controlador del navegador (ajusta la ruta al controlador, por defecto busca en al directorio raiz)
    # Recuerda verificar que chromedriver.exe sea compatible con tu actual version de Chrome
    driver = selenium.webdriver.Chrome()  # Si tienes chromedriver.exe en otra ubicación, especifícala.

    for i in range(len(supermercados)):
        producto = producto[i]
        supermercado = supermercados[i]
        url = urls[i]
        selector = selectores[i]
        imagen_producto = imagenes[i]

        try:
            # Abre la pagina en el navegador
            driver.get(url)

            # Espera hasta que el elemento con el selector este presente en la pagina
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, selector)))

            # Encuentra el elemento que contiene el precio
            precio_element = driver.find_element(By.CLASS_NAME, selector)

            if precio_element:
                precio_text = precio_element.text.strip()
                precio_limpio = re.sub(r'[^\d.]', '', precio_text)

                # Genera un identificador unico para el resultado
                resultado_id = str(uuid.uuid4())

                resultado = {
                    "ID": resultado_id,
                    "Producto": producto,
                    "Supermercado": supermercado,
                    "Precio": precio_limpio,
                    "URL": url,
                    "Imagen": imagen_producto
                }
                resultados.append(resultado)

        except Exception as e:
            print("Error en la solicitud:", e)

    # Cierra el navegador al finalizar
    driver.quit()

    return resultados



