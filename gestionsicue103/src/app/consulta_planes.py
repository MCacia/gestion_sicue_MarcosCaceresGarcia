import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Función para conectar a la base de datos y manejar la conexión
def conectar_db():
    return sqlite3.connect('../db/sicue.db', timeout=10)

# Función para realizar la consulta de los planes de convalidación
def consultar_planes():
    # Realizar la consulta a la base de datos
    with conectar_db() as conn:
        c = conn.cursor()

        # Consulta para obtener todos los planes de convalidación
        c.execute("""
            SELECT universidad_origen, universidad_destino, duracion, asignaturas
            FROM planes_convalidacion
        """)
        planes = c.fetchall()

    # Si no se encuentran planes de convalidación
    if not planes:
        messagebox.showinfo("Resultado", "No se encontraron planes de convalidación.")
        return

    # Limpiar la lista de resultados anteriores
    for row in treeview.get_children():
        treeview.delete(row)

    # Agregar los resultados a la vista de la tabla
    for plan in planes:
        treeview.insert("", "end", values=plan)

# Crear la ventana principal
root = tk.Tk()
root.title("Consulta de Planes de Convalidación")
root.geometry("700x500")  # Establecer tamaño inicial de la ventana
root.resizable(True, True)  # Hacer la ventana redimensionable

# Botón para realizar la consulta
button_consultar = tk.Button(root, text="Consultar Planes de Convalidación", command=consultar_planes, font=("Arial", 12))
button_consultar.grid(row=0, column=0, columnspan=2, pady=10)

# Crear un Treeview para mostrar los resultados
treeview = ttk.Treeview(root, columns=("Universidad Origen", "Universidad Destino", "Duración", "Asignaturas"), show="headings", height=15)
treeview.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Definir las columnas de la tabla
treeview.heading("Universidad Origen", text="Universidad Origen")
treeview.heading("Universidad Destino", text="Universidad Destino")
treeview.heading("Duración", text="Duración")
treeview.heading("Asignaturas", text="Asignaturas")

# Ajustar el ancho de las columnas
treeview.column("Universidad Origen", width=150)
treeview.column("Universidad Destino", width=150)
treeview.column("Duración", width=100)
treeview.column("Asignaturas", width=200)

# Configurar el grid para que sea redimensionable
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()



