from fastapi import FastAPI
from scrap3super import scrap_tallarines

app = FastAPI()

@app.get("/")
def mostrar_informacion():
    resultado = scrap_tallarines()

    return {
        "Nombre del Producto": "Tallarines",
        "Supermercado": resultado["Supermercado"],
        "Precio Más Bajo": resultado["Precio"],
        "URL Acortada": resultado["URL"][:10]
    }
