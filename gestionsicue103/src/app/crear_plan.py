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

# Crear la ventana principal
root = tk.Tk()
root.title("Crear Plan de Convalidación")
root.geometry("800x600")  # Establecer tamaño inicial de la ventana
root.resizable(True, True)  # Hacer la ventana redimensionable

# Etiquetas y campos de entrada para el plan de convalidación
label_origen = tk.Label(root, text="Universidad de Origen:", font=("Arial", 12))
label_origen.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_origen = tk.Entry(root, font=("Arial", 12))
entry_origen.grid(row=0, column=1, padx=10, pady=5, sticky="w")

label_destino = tk.Label(root, text="Universidad de Destino:", font=("Arial", 12))
label_destino.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_destino = tk.Entry(root, font=("Arial", 12))
entry_destino.grid(row=1, column=1, padx=10, pady=5, sticky="w")

label_duracion = tk.Label(root, text="Duración del Plan (en meses):", font=("Arial", 12))
label_duracion.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_duracion = tk.Entry(root, font=("Arial", 12))
entry_duracion.grid(row=2, column=1, padx=10, pady=5, sticky="w")

label_asignaturas = tk.Label(root, text="Asignaturas a Convalidar (separadas por coma):", font=("Arial", 12))
label_asignaturas.grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_asignaturas = tk.Entry(root, font=("Arial", 12))
entry_asignaturas.grid(row=3, column=1, padx=10, pady=5, sticky="w")

label_asignaturas_convalidadas = tk.Label(root, text="Asignaturas Convalidadas (separadas por coma):", font=("Arial", 12))
label_asignaturas_convalidadas.grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_asignaturas_convalidadas = tk.Entry(root, font=("Arial", 12))
entry_asignaturas_convalidadas.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Botón para crear el plan de convalidación
button_crear_plan = tk.Button(root, text="Crear Plan de Convalidación", command=crear_plan_convalidacion, font=("Arial", 12))
button_crear_plan.grid(row=5, column=0, columnspan=2, pady=10)

# Configurar el grid para que sea redimensionable
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
