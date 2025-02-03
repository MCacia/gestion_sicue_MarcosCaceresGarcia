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

def obtener_planes_convalidacion():
    """Obtiene los planes de convalidación existentes de la base de datos."""
    with conectar_db() as conn:
        c = conn.cursor()
        c.execute("SELECT id, universidad_origen, universidad_destino FROM planes_convalidacion")
        return c.fetchall()

def cargar_datos_plan(event):
    """Carga los datos del plan seleccionado en los campos de entrada."""
    seleccionado = combo_planes.get()
    if not seleccionado:
        return
    
    plan_id = seleccionado.split(" - ")[0]  # Obtener el ID del plan
    
    with conectar_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM planes_convalidacion WHERE id = ?", (plan_id,))
        plan = c.fetchone()
    
    if plan:
        entry_origen.delete(0, tk.END)
        entry_origen.insert(0, plan[1])
        entry_destino.delete(0, tk.END)
        entry_destino.insert(0, plan[2])
        entry_duracion.delete(0, tk.END)
        entry_duracion.insert(0, plan[3])
        entry_asignaturas.delete(0, tk.END)
        entry_asignaturas.insert(0, plan[4])
        entry_asignaturas_convalidadas.delete(0, tk.END)
        entry_asignaturas_convalidadas.insert(0, plan[5])

def modificar_plan_convalidacion():
    """Modifica el plan de convalidación seleccionado."""
    seleccionado = combo_planes.get()
    if not seleccionado:
        messagebox.showerror("Error", "Seleccione un plan de convalidación.")
        return
    
    plan_id = seleccionado.split(" - ")[0]
    universidad_origen = entry_origen.get()
    universidad_destino = entry_destino.get()
    duracion = entry_duracion.get()
    asignaturas = entry_asignaturas.get()
    asignaturas_convalidadas = entry_asignaturas_convalidadas.get()

    if not universidad_origen or not universidad_destino or not duracion or not asignaturas or not asignaturas_convalidadas:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return
    
    with conectar_db() as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE planes_convalidacion 
            SET universidad_origen = ?, universidad_destino = ?, duracion = ?, asignaturas = ?, asignaturas_convalidadas = ?
            WHERE id = ?
        """, (universidad_origen, universidad_destino, duracion, asignaturas, asignaturas_convalidadas, plan_id))
        conn.commit()
    
    messagebox.showinfo("Éxito", "Plan de convalidación modificado con éxito.")

root = tk.Tk()
root.title("Modificar Plan de Convalidación")
root.geometry("800x600")
root.resizable(True, True)

label_planes = tk.Label(root, text="Seleccionar Plan de Convalidación:", font=("Arial", 12))
label_planes.grid(row=0, column=0, padx=10, pady=5, sticky="e")

planes = obtener_planes_convalidacion()
combo_planes = ttk.Combobox(root, font=("Arial", 12), values=[f"{p[0]} - {p[1]} -> {p[2]}" for p in planes])
combo_planes.grid(row=0, column=1, padx=10, pady=5, sticky="w")
combo_planes.bind("<<ComboboxSelected>>", cargar_datos_plan)

label_origen = tk.Label(root, text="Universidad de Origen:", font=("Arial", 12))
label_origen.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_origen = tk.Entry(root, font=("Arial", 12))
entry_origen.grid(row=1, column=1, padx=10, pady=5, sticky="w")

label_destino = tk.Label(root, text="Universidad de Destino:", font=("Arial", 12))
label_destino.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_destino = tk.Entry(root, font=("Arial", 12))
entry_destino.grid(row=2, column=1, padx=10, pady=5, sticky="w")

label_duracion = tk.Label(root, text="Duración del Plan (en meses):", font=("Arial", 12))
label_duracion.grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_duracion = tk.Entry(root, font=("Arial", 12))
entry_duracion.grid(row=3, column=1, padx=10, pady=5, sticky="w")

label_asignaturas = tk.Label(root, text="Asignaturas a Convalidar:", font=("Arial", 12))
label_asignaturas.grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_asignaturas = tk.Entry(root, font=("Arial", 12))
entry_asignaturas.grid(row=4, column=1, padx=10, pady=5, sticky="w")

label_asignaturas_convalidadas = tk.Label(root, text="Asignaturas Convalidadas:", font=("Arial", 12))
label_asignaturas_convalidadas.grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_asignaturas_convalidadas = tk.Entry(root, font=("Arial", 12))
entry_asignaturas_convalidadas.grid(row=5, column=1, padx=10, pady=5, sticky="w")

button_modificar_plan = tk.Button(root, text="Modificar Plan de Convalidación", command=modificar_plan_convalidacion, font=("Arial", 12))
button_modificar_plan.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
