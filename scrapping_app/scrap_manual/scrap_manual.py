import tkinter as tk
import os
import sys
from tkinter import simpledialog, messagebox, ttk, PhotoImage
import mysql.connector
from datetime import datetime
from data import DATA
import webbrowser
from dicts import supermercado_ids, producto_ids
from PIL import Image, ImageTk


# Lista para almacenar datos temporalmente
datos_a_insertar = []

def reiniciar_app():
    """ Pregunta al usuario antes de reiniciar el script de Python. """
    respuesta = messagebox.askyesno("Reiniciar Aplicacion", "Se actualizara la app, cualquier dato no guardado se perdera. ¿Desea actualizar? NO LLORES LUEGO")
    if respuesta:
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
        
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
        messagebox.showinfo("Informacion", "No hay datos para insertar.")
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
        self.iconbitmap('scrapping_app/scrap_manual/images/bird-1.ico')
        self.configure(background='white')  # Cambiar el color de fondo
        self.grab_set()  # Hace que la ventana sea modal
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Manejar el evento de cierre de ventana
        
    def on_close(self):
        # Se llamará a esta función cuando el usuario intente cerrar la ventana de diálogo
        self.on_cancel()
        
    def set_window_position(self):
        window_width = 400
        window_height = 150
        # Puedes ajustar estas coordenadas para cambiar la posición de la ventana
        position_right = 50
        position_down = 50
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_down}')

    def create_widgets(self):
        tk.Label(self, text=self.message).pack(pady=(20, 10))
        self.entry = tk.Entry(self)
        self.entry.pack(pady=5, padx=20, fill='x', expand=True)
        # Botón Aceptar
        button_accept = tk.Button(self, text="Aceptar", command=self.on_accept)
        button_accept.pack(side="left", padx=(20, 10), pady=(0, 20), fill='x', expand=True)
        # Botón Cancelar
        button_cancel = tk.Button(self, text="Cancelar", command=self.on_cancel)
        button_cancel.pack(side="right", padx=(10, 20), pady=(0, 20), fill='x', expand=True)

    def on_accept(self):
        try:
            self.precio = int(self.entry.get())
            self.destroy()
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingrese valores validos, no sea pelmazo.")

    def on_cancel(self):
        if messagebox.askyesno("Confirmacion", "Desea cancelar el scraping?"):
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
    
def iniciar_scrap(iid):
    selected_item = tabla.focus()
    valores = tabla.item(selected_item, 'values')
    supermercado, producto = valores[0], valores[1]
    info = DATA[producto][supermercado]

    # Abrir el URL para scraping
    abrir_url(info['Link'])

    # Crear y mostrar la ventana de diálogo personalizada
    dialog = CustomDialog(app, "Ingresar Precio", f"Ingrese el precio para {producto} en {supermercado}")
    app.wait_window(dialog)

    # Obtener el precio desde el diálogo
    nuevo_precio = dialog.precio

    if nuevo_precio is not None:
        # Actualizar visualmente la tabla con el nuevo precio
        tabla.item(selected_item, values=(supermercado, producto, valores[2], nuevo_precio))

        # Añadir o actualizar el dato en la lista de datos a insertar
        producto_id = obtener_id_producto(producto)
        supermercado_id = obtener_id_supermercado(supermercado)
        
        # Encuentra el dato en datos_a_insertar o lo añade si es nuevo
        encontrado = False
        for i, (p_id, s_id, _) in enumerate(datos_a_insertar):
            if p_id == producto_id and s_id == supermercado_id:
                datos_a_insertar[i] = (producto_id, supermercado_id, nuevo_precio)
                encontrado = True
                break
        
        if not encontrado:
            datos_a_insertar.append((producto_id, supermercado_id, nuevo_precio))

        # Mostrar mensaje de confirmación
        messagebox.showinfo("Confirmación", f"El precio para {producto} en {supermercado} ha sido actualizado a {nuevo_precio}")




def mostrar_menu_contextual(event):
    menu_contextual = tk.Menu(app, tearoff=0)
    iid = tabla.identify_row(event.y)
    if iid:
        tabla.selection_set(iid)
        menu_contextual.add_command(label="Iniciar Scrap Individual", command=lambda: iniciar_scrap(iid))
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
    respuesta = messagebox.askyesno("Borrar Precios Actualizados", "Seguro que desea borrar los precios actualizados? \nEsta accion no tiene vuelta atras.")
    if respuesta:
        # Limpia la visualización de precios en la tabla
        for child in tabla.get_children():
            values = tabla.item(child, 'values')
            tabla.item(child, values=(values[0], values[1], values[2], ""))  # Establecer el precio actualizado en vacío
        # Limpia los datos en la lista para prevenir la inserción
        datos_a_insertar.clear()

def ajustar_tamaño_columnas(event=None):
    ancho_tabla = tabla.winfo_width()  # Obtener el ancho actual de la tabla
    num_columnas = len(tabla["columns"])
    ancho_columna = ancho_tabla // num_columnas
    for columna in tabla["columns"]:
        tabla.column(columna, width=ancho_columna)
        
def cargar_y_redimensionar_imagen(ruta_imagen, nuevo_ancho, nuevo_alto):
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(imagen)
        
def mostrar_menu_principal():
    global tabla
    for widget in app.winfo_children():
        widget.destroy()

    # Configuración del Frame de botones a la izquierda
    botones_frame = tk.Frame(app, bg='white')
    botones_frame.grid(row=0, column=0, sticky='ns')
    
    # Carga y redimensiona la imagen
    imagen_redimensionada = cargar_y_redimensionar_imagen('scrapping_app/scrap_manual/images/bird-1.png', 100, 100)

    # Crea un Label para la imagen y lo coloca en el Frame
    label_imagen = tk.Label(botones_frame, image=imagen_redimensionada, bg='white')
    label_imagen.image = imagen_redimensionada  # Referencia para evitar la recolección de basura
    label_imagen.grid(row=0, column=0, padx=10, pady=10)  # Imagen en la fila 0

    # Botones con tamaño personalizado
    boton_scraping = tk.Button(botones_frame, text="Comenzar Scraping", command=extraer_precios, background='#39BE2C', highlightbackground='green', width=20, height=2)
    boton_scraping.grid(row=1, column=0, padx=10, pady=10)  # Botón "Comenzar Scraping" en la fila 1

    boton_insertar = tk.Button(botones_frame, text="Confirmar Ingreso Precios \n Actualizados", command=insertar_datos, background='#59CDC2', highlightbackground='lightblue', width=20, height=2)
    boton_insertar.grid(row=2, column=0, padx=10, pady=10)  # Botón "Insertar Nuevos Datos" en la fila 2

    boton_borrar = tk.Button(botones_frame, text="Borrar todo los Datos \n Actualizados.", command=limpiar_precios_actualizados, background='#E74A5F', highlightbackground='red', width=20, height=2)
    boton_borrar.grid(row=3, column=0, padx=10, pady=10)  # Botón "Borrar todo los Datos" en la fila 3
    
    # Botón para reiniciar la aplicación
    boton_reiniciar = tk.Button(botones_frame, text="Refrescar Datos", command=reiniciar_app, background='#E26ADB', highlightbackground='lightblue', width=20, height=2)
    boton_reiniciar.grid(row=4, column=0, padx=10, pady=10)  # Botón "Refrescar Datos" en la fila 4
    
    leyenda_frame = tk.Frame(app, bg='white')
    leyenda_frame.grid(row=5, column=0, sticky='ew')  # Frame de la leyenda en la fila 5


    # Configuración de la tabla
    tabla = ttk.Treeview(app, columns=("Supermercado", "Producto", "Último Precio", "Precio Actualizado"), show='headings', height=28)
    tabla.heading("Supermercado", text="Supermercado")
    tabla.heading("Producto", text="Producto")
    tabla.heading("Último Precio", text="Último Precio")
    tabla.heading("Precio Actualizado", text="Precio Actualizado")
    tabla.grid(row=0, column=1, sticky='nsew')
    # Definir etiquetas con estilos
    tabla.tag_configure('oddrow', background='white')
    tabla.tag_configure('evenrow', background='#D1DEF1')


    # Configuración de la barra de desplazamiento
    scrollbar = ttk.Scrollbar(app, orient="vertical", command=tabla.yview)
    scrollbar.grid(row=0, column=2, sticky='ns')
    tabla.configure(yscrollcommand=scrollbar.set)

    # Configuración del layout
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    
        # Ajustar el tamaño de las columnas al inicio y cuando la ventana se redimensiona
    app.after(100, ajustar_tamaño_columnas)  # Ajustar tamaño después de que la ventana esté visible
    app.bind("<Configure>", ajustar_tamaño_columnas)

    # Cargar los datos iniciales en la tabla
    cargar_datos_iniciales()

    tabla.bind("<Button-3>", mostrar_menu_contextual)

def cargar_datos_iniciales():
    ultimos_precios = obtener_todos_los_ultimos_precios()
    count = 0  # Contador para alternar las etiquetas
    for producto, supermercados in DATA.items():
        for supermercado in supermercados:
            producto_id = obtener_id_producto(producto)
            supermercado_id = obtener_id_supermercado(supermercado)
            ultimo_precio = ultimos_precios.get((producto_id, supermercado_id), 'N/A')

            # Convertir el precio a entero si no es 'N/A'
            if ultimo_precio != 'N/A':
                ultimo_precio = int(ultimo_precio)

            # Aplicar etiqueta según sea fila par o impar
            if count % 2 == 0:
                tabla.insert('', 'end', values=(supermercado, producto, ultimo_precio, ""), tags=('evenrow',))
            else:
                tabla.insert('', 'end', values=(supermercado, producto, ultimo_precio, ""), tags=('oddrow',))

            count += 1
            
# En tu función principal o en la configuración inicial de la ventana
app = tk.Tk()
app.title("MartinMercado@ Software de Actualización de Precios V2.0")
# Establece la posición de la ventana en el tope de la pantalla (puedes ajustar la posición en x según lo necesites)
app.geometry("720x770+0+0")
app.configure(bg='white')
icon = PhotoImage(file='scrapping_app/static/assets/favicon-32x32.png')
app.iconphoto(False, icon)
mostrar_menu_principal()
app.mainloop()
