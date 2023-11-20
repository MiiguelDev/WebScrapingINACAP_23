import tkinter as tk
from tkinter import simpledialog, messagebox
import mysql.connector
from datetime import datetime
from data import DATA

# Diccionarios con los IDs
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

def obtener_id_supermercado(nombre_supermercado):
    """
    Devuelve el ID correspondiente al nombre del supermercado.
    """
    return supermercado_ids.get(nombre_supermercado, None)

def obtener_id_producto(nombre_producto):
    """
    Devuelve el ID correspondiente al nombre del producto.
    """
    return producto_ids.get(nombre_producto, None)


# Función para insertar datos en la base de datos
def insertar_datos(datos_a_insertar):
    try:
        con = mysql.connector.connect(
            host="3.22.156.122",
            user="scrapy",
            password="Inacap2023#",
            database="comparacion_precios"

        )
        cursor = con.cursor()

        for dato in datos_a_insertar:
            producto, supermercado, precio = dato
            supermercado_id = obtener_id_supermercado(supermercado)
            producto_id = obtener_id_producto(producto)
            fecha_hora_actual = datetime.now()

            query = "INSERT INTO historial_precios (super_id, producto_id, precio, fecha_hora) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (supermercado_id, producto_id, precio, fecha_hora_actual))

        con.commit()
        messagebox.showinfo("Éxito", "Datos insertados correctamente")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

# Función para procesar y mostrar los datos para confirmación
def procesar_datos():
    datos_a_insertar = []
    for producto, supermercados in DATA.items():
        for supermercado, info in supermercados.items():
            precio = simpledialog.askinteger("Ingresar Precio", f"Ingrese el precio para {producto} en {supermercado}:")
            if precio is not None:
                datos_a_insertar.append((producto, supermercado, precio))

    confirmacion = messagebox.askyesno("Confirmación", "¿Desea insertar los siguientes datos?\n" + "\n".join([f"{d[0]} - {d[1]}: {d[2]}" for d in datos_a_insertar]))

    if confirmacion:
        insertar_datos(datos_a_insertar)
    else:
        messagebox.showinfo("Cancelado", "Inserción cancelada")

# Creación de la ventana de la aplicación
app = tk.Tk()
app.title("Inserción de Datos de Precios")

# Botón para iniciar el procesamiento de datos
button_procesar = tk.Button(app, text="Ingresar Precios", command=procesar_datos)
button_procesar.pack()

# Iniciar la aplicación
app.mainloop()
