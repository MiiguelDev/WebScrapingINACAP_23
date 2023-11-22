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

# Lista para almacenar datos temporalmente
datos_a_insertar = []

def obtener_id_supermercado(nombre_supermercado):
    return supermercado_ids.get(nombre_supermercado, None)

def obtener_id_producto(nombre_producto):
    return producto_ids.get(nombre_producto, None)

def obtener_todos_los_ultimos_precios():
    try:
        con = mysql.connector.connect(
            host="3.22.156.122",
            user="scrapy",
            password="Inacap2023#",
            database="comparacion_precios"
        )
        cursor = con.cursor()
        query = """
            SELECT hp.producto_id, hp.super_id, hp.precio
            FROM historial_precios AS hp
            INNER JOIN (
                SELECT producto_id, super_id, MAX(fecha_hora) AS max_fecha_hora
                FROM historial_precios
                GROUP BY producto_id, super_id
            ) AS max_prices ON hp.producto_id = max_prices.producto_id AND hp.super_id = max_prices.super_id AND hp.fecha_hora = max_prices.max_fecha_hora
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return {(row[0], row[1]): row[2] for row in resultados}
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

# Lista para almacenar datos temporalmente
datos_a_insertar = []

def insertar_datos():
    # Esta función insertará los datos almacenados en 'datos_a_insertar' en la base de datos
    if not datos_a_insertar:
        messagebox.showinfo("Información", "No hay datos para insertar.")
        return
    
    try:
        con = mysql.connector.connect(
            host="3.22.156.122",
            user="scrapy",
            password="Inacap2023#",
            database="comparacion_precios"
        )
        cursor = con.cursor()

        for dato in datos_a_insertar:
            producto_id, supermercado_id, precio = dato

            # Asegúrate de que tanto producto_id como supermercado_id no son None antes de insertar
            if producto_id is not None and supermercado_id is not None:
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


def abrir_url(url):
    webbrowser.open(url)

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.message = message
        self.parent = parent
        self.precio = None
        self.create_widgets()
        self.set_window_position()
        self.configure(background='#4F7BA7')  # Cambiar el color de fondo
        self.grab_set()  # Hace que la ventana sea modal
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Manejar el evento de cierre de ventana
        
    def on_close(self):
        # Se llamará a esta función cuando el usuario intente cerrar la ventana de diálogo
        self.on_cancel()
        
    def set_window_position(self):
        window_width = 700  # Ancho fijo de la ventana
        window_height = 175  # Alto fijo de la ventana

        # Obtener las dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular la posición x e y
        x = 50  # A la izquierda de la pantalla
        y = (screen_height - window_height) // 2  # En el centro de la pantalla verticalmente

        # Configurar tamaño y posición
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def create_widgets(self):
        tk.Label(self, text=self.message).pack(pady=10)
        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)
        tk.Button(self, text="Aceptar", command=self.on_accept).pack(side="left", padx=(20, 10), pady=10)
        tk.Button(self, text="Cancelar", command=self.on_cancel).pack(side="right", padx=(10, 20), pady=10)

    def on_accept(self):
        try:
            self.precio = int(self.entry.get())
            self.destroy()
        except ValueError:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un número válido.")

    def on_cancel(self):
        if messagebox.askyesno("Confirmación", "Desea cancelar el scraping?"):
            self.parent.cancel_scraping = True
            self.destroy()

def extraer_precios():
    app.cancel_scraping = False
    ultimos_precios = obtener_todos_los_ultimos_precios()

    for child in tabla.get_children():
        values = tabla.item(child, 'values')
        supermercado, producto, ultimo_precio, precio_actualizado = values
        if precio_actualizado:  # Si ya hay un precio actualizado, saltar al siguiente
            continue

        info = DATA[producto][supermercado]
        abrir_url(info['Link'])
        dialog = CustomDialog(app, "Ingresar Precio", f"Ingrese el precio para {producto} en {supermercado}")
        app.wait_window(dialog)
        precio = dialog.precio

        if precio is not None:
            tabla.item(child, values=(supermercado, producto, ultimo_precio, precio))
            producto_id = obtener_id_producto(producto)
            supermercado_id = obtener_id_supermercado(supermercado)
            datos_a_insertar.append((producto_id, supermercado_id, precio))
        elif app.cancel_scraping:
            break

def editar_precio_actualizado(iid):
    selected_item = tabla.focus()
    valores = tabla.item(selected_item, 'values')
    supermercado, producto = valores[0], valores[1]
    producto_id = obtener_id_producto(producto)
    supermercado_id = obtener_id_supermercado(supermercado)

    nuevo_precio = simpledialog.askinteger("Editar Precio", "Ingrese el nuevo precio:", parent=app)
    if nuevo_precio is not None:
        # Actualiza visualmente la tabla
        tabla.item(selected_item, values=(supermercado, producto, valores[2], nuevo_precio))

        # Encuentra el dato en datos_a_insertar o lo añade si es nuevo
        encontrado = False
        for i, (p_id, s_id, _) in enumerate(datos_a_insertar):
            if p_id == producto_id and s_id == supermercado_id:
                datos_a_insertar[i] = (producto_id, supermercado_id, nuevo_precio)
                encontrado = True
                break
        
        if not encontrado:
            datos_a_insertar.append((producto_id, supermercado_id, nuevo_precio))

def borrar_precio_actualizado(iid):
    selected_item = tabla.focus()
    valores = tabla.item(selected_item, 'values')
    supermercado, producto = valores[0], valores[1]
    producto_id = obtener_id_producto(producto)
    supermercado_id = obtener_id_supermercado(supermercado)

    # Actualiza visualmente la tabla
    tabla.item(selected_item, values=(supermercado, producto, valores[2], ""))

    # Encuentra y borra el dato en datos_a_insertar
    datos_a_insertar[:] = [(p_id, s_id, precio) for p_id, s_id, precio in datos_a_insertar if not (p_id == producto_id and s_id == supermercado_id)]


def mostrar_menu_contextual(event):
    menu_contextual = tk.Menu(app, tearoff=0)
    iid = tabla.identify_row(event.y)
    if iid:
        tabla.selection_set(iid)
        menu_contextual.add_command(label="Editar Precio Actualizado", command=lambda: editar_precio_actualizado(iid))
        menu_contextual.add_command(label="Borrar Precio Actualizado", command=lambda: borrar_precio_actualizado(iid))
        menu_contextual.tk_popup(event.x_root, event.y_root)


            
def on_edit_precio(event):
    # Obtener la fila seleccionada
    selected_item = tabla.focus()
    if not selected_item:
        return

    # Crear una pequeña ventana de diálogo para la edición
    precio_edit_dialog = simpledialog.askinteger("Editar Precio", "Nuevo precio:", parent=app)
    if precio_edit_dialog is not None:
        tabla.item(selected_item, values=(tabla.item(selected_item, 'values')[0], 
                                          tabla.item(selected_item, 'values')[1], 
                                          tabla.item(selected_item, 'values')[2], 
                                          precio_edit_dialog))


def limpiar_precios_actualizados():
    respuesta = messagebox.askyesno("Borrar Precios Actualizados", "¿Está seguro de que quiere borrar todos los precios actualizados?")
    if respuesta:
        # Limpia la visualización de precios en la tabla
        for child in tabla.get_children():
            values = tabla.item(child, 'values')
            tabla.item(child, values=(values[0], values[1], values[2], ""))  # Establecer el precio actualizado en vacío
        # Limpia los datos en la lista para prevenir la inserción
        datos_a_insertar.clear()


def mostrar_menu_principal():
    global tabla
    for widget in app.winfo_children():
        widget.destroy()

    tabla = ttk.Treeview(app, columns=("Supermercado", "Producto", "Último Precio", "Precio Actualizado"), show='headings', height=28)
    tabla.heading("Supermercado", text="Supermercado")
    tabla.heading("Producto", text="Producto")
    tabla.heading("Último Precio", text="Último Precio")
    tabla.heading("Precio Actualizado", text="Precio Actualizado")

    ultimos_precios = obtener_todos_los_ultimos_precios()
    for producto, supermercados in DATA.items():
        for supermercado in supermercados:
            producto_id = obtener_id_producto(producto)
            supermercado_id = obtener_id_supermercado(supermercado)
            ultimo_precio = ultimos_precios.get((producto_id, supermercado_id), 'N/A')
            tabla.insert('', 'end', values=(supermercado, producto, ultimo_precio, ""))  # Inicialmente no hay precio actualizado

    scrollbar = ttk.Scrollbar(app, orient="vertical", command=tabla.yview)
    scrollbar.pack(side='right', fill='y')
    tabla.configure(yscrollcommand=scrollbar.set)
    tabla.pack(expand=True, fill='both')

    botones_frame = tk.Frame(app, bg='#4F7BA7')
    botones_frame.pack(fill='x')

    boton_scraping = tk.Button(botones_frame, text="Comenzar scraping", command=extraer_precios, background='green', highlightbackground='green')
    boton_scraping.pack(side=tk.LEFT, padx=(20, 10), pady=10)

    boton_insertar = tk.Button(botones_frame, text="Insertar Datos", command=insertar_datos, background='lightblue', highlightbackground='lightblue')
    boton_insertar.pack(side=tk.LEFT, padx=(10, 20), pady=10)

    boton_borrar = tk.Button(botones_frame, text="Borrar todo los precios act.", command=limpiar_precios_actualizados, background='red', highlightbackground='red')
    boton_borrar.pack(side=tk.LEFT, padx=(10, 20), pady=10)
    
    tabla.bind("<Button-3>", mostrar_menu_contextual)


app = tk.Tk()
app.title("MartinMercado /// Actualización de Precios")
app.geometry("800x700")
app.configure(bg='#4F7BA7')
icon = PhotoImage(file='scrapping_app/static/assets/favicon-32x32.png')
app.iconphoto(False, icon)
mostrar_menu_principal()
app.mainloop()