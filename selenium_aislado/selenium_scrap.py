import mysql.connector
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from data import DATA
import time

# Este codigo actualmente no funciona al 100% ya que Jumbo y Sta Isabel cambiaron la estructura de sus paginas recientemente.
def scrap_product_info_to_database(supermercados, productos, data_dict):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="comparacion_precios"
    )
    # '3.22.156.122', 'comparacion_precios', 'scrapy', 'Inacap2023#'
    mycursor = mydb.cursor()

    producto_ids = {
        'Aceite': 1,
        'Azucar': 2,
        'Atun': 3,
        'Lavalozas': 4,
        'Agua': 5,
    }
    supermercado_ids = {
        'Lider': 1,
        'Jumbo': 2,
        'Santa Isabel': 3,
        'Cugat': 4,
    }

    for producto_nombre in productos:
        producto_id = producto_ids.get(producto_nombre)

        for supermercado in supermercados:
            supermercado_id = supermercado_ids.get(supermercado)
            supermercado_info = data_dict.get(producto_nombre, {}).get(supermercado)

            if supermercado_info:
                url = supermercado_info.get("Link")
                selector = supermercado_info.get("Selector")

                driver = None
                try:
                    driver = webdriver.Chrome()
                    driver.get(url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, selector)))
                    precio_element = driver.find_element(By.CLASS_NAME, selector)

                    if precio_element:
                        precio_text = precio_element.text.strip()
                        precio_limpio = re.sub(r'[^\d]+', '', precio_text)

                        timestamp = datetime.now()
                        sql = "INSERT INTO historial_precios (super_id, producto_id, precio, fecha_hora) VALUES (%s, %s, %s, %s)"
                        val = (supermercado_id, producto_id, precio_limpio, timestamp)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        print(f"Insertado: Supermercado ID {supermercado_id}, Producto ID {producto_id}, Precio {precio_limpio}, Fecha {timestamp}")

                except Exception as e:
                    print("Error en la solicitud:", e)
                finally:
                    if driver:
                        driver.quit()
                    time.sleep(2)

    mydb.close()

# Llama a la función con los datos de scrapping
scrap_product_info_to_database(
    supermercados=['Lider', 'Jumbo', 'Santa Isabel', 'Cugat'],
    productos=['Aceite', 'Azucar', 'Atun', 'Lavalozas', 'Agua'],
    data_dict=DATA
)

