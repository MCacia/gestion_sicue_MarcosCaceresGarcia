import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys

# Establecer el directorio raíz del programa
directorio_raiz = os.path.abspath(os.path.join(os.getcwd(), "../../../gestionsicue103"))

try:
    os.chdir(directorio_raiz)
except FileNotFoundError:
    print(f"Error: No se pudo encontrar el directorio {directorio_raiz}")
    sys.exit(1)

# Asegurarse de que el directorio 'src' está en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))

from utils.conectar_db import conectar_db  # Importar la función modularizada

# Función para crear un plan de convalidación
def crear_plan_convalidacion():
    universidad_origen = entry_origen.get()
    universidad_destino = entry_destino.get()
    duracion = entry_duracion.get()
    asignaturas = entry_asignaturas.get()
    asignaturas_convalidadas = entry_asignaturas_convalidadas.get()

    # Validar si todos los campos están llenos
    if not universidad_origen or not universidad_destino or not duracion or not asignaturas or not asignaturas_convalidadas:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    # Usamos 'with' para manejar la conexión y evitar problemas de bloqueo
    with conectar_db() as conn:
        c = conn.cursor()

        # Insertar el plan de convalidación en la base de datos
        c.execute("""
            INSERT INTO planes_convalidacion (universidad_origen, universidad_destino, duracion, asignaturas, asignaturas_convalidadas)
            VALUES (?, ?, ?, ?, ?)
        """, (universidad_origen, universidad_destino, duracion, asignaturas, asignaturas_convalidadas))
        conn.commit()

    messagebox.showinfo("Éxito", "Plan de convalidación creado con éxito.")
    # Limpiar los campos de entrada después de crear el plan
    entry_origen.delete(0, tk.END)
    entry_destino.delete(0, tk.END)
    entry_duracion.delete(0, tk.END)
    entry_asignaturas.delete(0, tk.END)
    entry_asignaturas_convalidadas.delete(0, tk.END)

# Función para agregar un profesor
def agregar_profesor():
    nombre = entry_nombre_profesor.get()
    correo = entry_correo_profesor.get()
    grado = entry_grado_profesor.get()

    # Validar si todos los campos están llenos
    if not nombre or not correo or not grado:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    # Usamos 'with' para manejar la conexión y evitar problemas de bloqueo
    with conectar_db() as conn:
        c = conn.cursor()

        # Insertar el profesor en la base de datos
        c.execute("""
            INSERT INTO profesores (nombre, correo, grado)
            VALUES (?, ?, ?)
        """, (nombre, correo, grado))
        conn.commit()

    messagebox.showinfo("Éxito", "Profesor agregado con éxito.")
    # Limpiar los campos de entrada después de agregar el profesor
    entry_nombre_profesor.delete(0, tk.END)
    entry_correo_profesor.delete(0, tk.END)
    entry_grado_profesor.delete(0, tk.END)

# Función para mostrar los profesores
def mostrar_profesores():
    with conectar_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM profesores")
        profesores = c.fetchall()

    # Limpiar la lista de resultados anteriores
    for row in treeview_profesores.get_children():
        treeview_profesores.delete(row)

    # Agregar los resultados a la vista de la tabla
    for profesor in profesores:
        treeview_profesores.insert("", "end", values=profesor)

# Crear la ventana principal
root = tk.Tk()
root.title("Crear Plan de Convalidación")

# Etiquetas y campos de entrada para el plan de convalidación
label_origen = tk.Label(root, text="Universidad de Origen:")
label_origen.grid(row=0, column=0, padx=10, pady=5)
entry_origen = tk.Entry(root)
entry_origen.grid(row=0, column=1, padx=10, pady=5)

label_destino = tk.Label(root, text="Universidad de Destino:")
label_destino.grid(row=1, column=0, padx=10, pady=5)
entry_destino = tk.Entry(root)
entry_destino.grid(row=1, column=1, padx=10, pady=5)

label_duracion = tk.Label(root, text="Duración del Plan (en meses):")
label_duracion.grid(row=2, column=0, padx=10, pady=5)
entry_duracion = tk.Entry(root)
entry_duracion.grid(row=2, column=1, padx=10, pady=5)

label_asignaturas = tk.Label(root, text="Asignaturas a Convalidar (separadas por coma):")
label_asignaturas.grid(row=3, column=0, padx=10, pady=5)
entry_asignaturas = tk.Entry(root)
entry_asignaturas.grid(row=3, column=1, padx=10, pady=5)

label_asignaturas_convalidadas = tk.Label(root, text="Asignaturas Convalidadas (separadas por coma):")
label_asignaturas_convalidadas.grid(row=4, column=0, padx=10, pady=5)
entry_asignaturas_convalidadas = tk.Entry(root)
entry_asignaturas_convalidadas.grid(row=4, column=1, padx=10, pady=5)

# Botón para crear el plan de convalidación
button_crear_plan = tk.Button(root, text="Crear Plan de Convalidación", command=crear_plan_convalidacion)
button_crear_plan.grid(row=5, column=0, columnspan=2, pady=10)

# Etiquetas y campos de entrada para agregar un profesor
label_nombre_profesor = tk.Label(root, text="Nombre del Profesor:")
label_nombre_profesor.grid(row=6, column=0, padx=10, pady=5)
entry_nombre_profesor = tk.Entry(root)
entry_nombre_profesor.grid(row=6, column=1, padx=10, pady=5)

label_correo_profesor = tk.Label(root, text="Correo del Profesor:")
label_correo_profesor.grid(row=7, column=0, padx=10, pady=5)
entry_correo_profesor = tk.Entry(root)
entry_correo_profesor.grid(row=7, column=1, padx=10, pady=5)

label_grado_profesor = tk.Label(root, text="Grado del Profesor:")
label_grado_profesor.grid(row=8, column=0, padx=10, pady=5)
entry_grado_profesor = tk.Entry(root)
entry_grado_profesor.grid(row=8, column=1, padx=10, pady=5)

# Botón para agregar el profesor
button_agregar_profesor = tk.Button(root, text="Agregar Profesor", command=agregar_profesor)
button_agregar_profesor.grid(row=9, column=0, columnspan=2, pady=10)

# Botón para mostrar los profesores
button_mostrar_profesores = tk.Button(root, text="Mostrar Profesores", command=mostrar_profesores)
button_mostrar_profesores.grid(row=10, column=0, columnspan=2, pady=10)

# Crear un Treeview para mostrar los profesores
treeview_profesores = ttk.Treeview(root, columns=("ID", "Nombre", "Correo", "Grado"), show="headings")
treeview_profesores.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

# Definir las columnas de la tabla
treeview_profesores.heading("ID", text="ID")
treeview_profesores.heading("Nombre", text="Nombre")
treeview_profesores.heading("Correo", text="Correo")
treeview_profesores.heading("Grado", text="Grado")

# Ajustar el ancho de las columnas
treeview_profesores.column("ID", width=50)
treeview_profesores.column("Nombre", width=150)
treeview_profesores.column("Correo", width=200)
treeview_profesores.column("Grado", width=100)

root.mainloop()

