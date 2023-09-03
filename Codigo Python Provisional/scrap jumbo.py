import requests
from bs4 import BeautifulSoup

def ScrapJumboTallarines():
    
    local = "Jumbo"

    url = "https://www.jumbo.cl/spaghetti-n-5-carozzi-bolsa-400-g-2/p"

    # Realizamos una solicitud GET para obtener el contenido de la web
    response = requests.get(url)

    # Verificamos si la solicitud fue exitosa (codigo 200)
    if response.status_code == 200:
        # Parseamos el contenido HTML usando BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Utilizamos select_one para encontrar el elemento que contiene el precio
        # Este valor varia dependiendo de la web, se debe "Inspeccionar elemento" y
        # buscar la linea especifica de donde extraer el valor
        # Ademas tener en cuenta que muchas webs actualizan los valores de manera dinamica
        # usando JS, en tal caso se debera usar Selenium para la extraccion.
        precio_element = soup.select_one('span.prices-main-price#scraping-tmp')

        if precio_element:
            # Extraemos el texto del elemento que contiene el precio
            precio = precio_element.text.strip()
    
    # Finalmente retornamos el precio y el local del que extrajimos los valores
    # Estos valores deben ser pasados a otra funcion que compare cada producto en cada local
    # y solo devuelva el nombre del local y el precio en que el producto esta mas barato.
    # Luego con los valores extraidos podemos armar la web "facilmente" ya que solo seria tener
    # una estructura que reciba valores actualizados cada x tiempo.  
    return f"Precio: {precio} - Local: {local}"

if __name__ == "__main__":
    print(ScrapJumboTallarines())
        
