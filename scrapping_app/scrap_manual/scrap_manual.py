import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, PhotoImage
import mysql.connector
from datetime import datetime
from data import DATA
import webbrowser

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
    return supermercado_ids.get(nombre_supermercado, None)

def obtener_id_producto(nombre_producto):
    return producto_ids.get(nombre_producto, None)


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
            print(supermercado_id)
            producto_id = obtener_id_producto(producto)
            print(producto_id)
            fecha_hora_actual = datetime.now()
            print(fecha_hora_actual)
            

            query = "INSERT INTO historial_precios (super_id, producto_id, precio, fecha_hora) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (supermercado_id, producto_id, precio, fecha_hora_actual))

        con.commit()
        messagebox.showinfo("Éxito!", "Datos insertados correctamente" + "\U0001F913" + "\U0001F913" + "\U0001F913")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


def abrir_url(url):
    webbrowser.open(url)

def extraer_precios():
    datos_a_insertar = []
    for producto, supermercados in DATA.items():
        for supermercado, info in supermercados.items():
            # Abrir la URL en el navegador
            abrir_url(info['Link'])

            # Mantener la ventana de Tkinter siempre al frente
            app.attributes("-topmost", True)
            precio = simpledialog.askinteger("Ingresar Precio -- " + "\U0001F9A5", 
                                             f"Ingrese el precio para {producto} en {supermercado}:\nURL: {info['Link']}",
                                             parent=app)
            app.attributes("-topmost", False)  # Volver a la configuración normal después de cerrar el diálogo

            if precio is not None:
                datos_a_insertar.append((producto, supermercado, precio))
                tabla.insert('', 'end', values=(producto, supermercado, info['Link'], precio))
            else:
                break

    if datos_a_insertar:
        confirmacion = messagebox.askyesno("Confirmación", "Desea insertar los siguientes datos?   "  + "\U0001F928" + "\U0001F928"+ "\U0001F928")
        if confirmacion:
            insertar_datos(datos_a_insertar)


def mostrar_menu_principal():
    # Limpiar la ventana
    for widget in app.winfo_children():
        widget.destroy()

    global tabla
    tabla = ttk.Treeview(app, columns=("Producto", "Supermercado", "URL", "Precio"), show='headings')
    tabla.heading("Producto", text="Producto")
    tabla.heading("Supermercado", text="Supermercado")
    tabla.heading("URL", text="URL")
    tabla.heading("Precio", text="Precio")
    tabla.pack(expand=True, fill='both')

    tk.Button(app, text="Extraer Precios", command=extraer_precios).pack(pady=20)

app = tk.Tk()
spaces = " " * 60
app.title("MartinMercado /// Actualización de Precios -- " + "\U0001F98D")
app.geometry("800x700+0+0")

# Cambiar el color de fondo
app.configure(bg='#4F7BA7')

# Establecer el ícono de la ventana usando PhotoImage
icon = PhotoImage(file='scrapping_app/static/assets/favicon-32x32.png')
app.iconphoto(False, icon)

mostrar_menu_principal()
app.mainloop()