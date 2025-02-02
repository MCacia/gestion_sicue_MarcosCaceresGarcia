import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys
import re

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

# Función para validar el DNI
def validar_dni(dni):
    """
    Valida el formato del DNI español.
    El DNI debe tener 8 dígitos seguidos de una letra.
    """
    pattern = re.compile(r'^\d{8}[A-Za-z]$')
    return pattern.match(dni) is not None

# Función para registrar la inscripción
def registrar_inscripcion():
    # Obtener los valores de los campos de entrada
    dni = entry_dni.get()
    nombre = entry_nombre.get()
    curso = entry_curso.get()
    plan_id = plan_ids[plan_combobox.get()]  # Obtener el plan_id correspondiente al nombre del plan

    # Verificar si los campos están vacíos
    if not dni or not nombre or not curso or not plan_id:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    # Validar el formato del DNI
    if not validar_dni(dni):
        messagebox.showerror("Error", "El formato del DNI no es válido. Debe tener 8 dígitos seguidos de una letra.")
        return

    # Comprobar si el alumno ya está inscrito en el mismo plan
    with conectar_db() as conn:
        c = conn.cursor()

        # Buscar si el alumno ya está inscrito en el plan
        c.execute("SELECT * FROM inscripciones WHERE estudiante_id = ? AND plan_id = ?", (dni, plan_id))
        existing_inscription = c.fetchone()

        if existing_inscription:
            messagebox.showerror("Error", "Este alumno ya está inscrito en este plan de convalidación.")
            return

        # Comprobar si el alumno existe en la tabla estudiantes
        c.execute("SELECT * FROM estudiantes WHERE dni=?", (dni,))
        alumno = c.fetchone()

        # Si el alumno NO existe, mostrar un mensaje de error
        if not alumno:
            messagebox.showerror("Error", "El DNI no está registrado en la base de datos de estudiantes.")
            return

        # Comprobar si el curso es 2º o 3º
        if curso != "2º" and curso != "3º":
            messagebox.showerror("Error", "Solo se puede inscribir alumnos de 2º o 3º.")
            return

        # Insertar la inscripción en la tabla de inscripciones
        c.execute("""
            INSERT INTO inscripciones (estudiante_id, plan_id, fecha_inscripcion)
            VALUES (?, ?, datetime('now'))
        """, (dni, plan_id))
        conn.commit()

    messagebox.showinfo("Éxito", "Inscripción realizada con éxito.")
    # Limpiar los campos de entrada después de la inscripción
    entry_dni.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_curso.delete(0, tk.END)
    plan_combobox.set('')

# Función para cargar los planes de convalidación desde la base de datos
def cargar_planes():
    with conectar_db() as conn:
        c = conn.cursor()
        c.execute("SELECT id, universidad_origen, universidad_destino FROM planes_convalidacion")
        planes = c.fetchall()

    # Crear dos listas: una con los nombres para mostrar y otra con los ids
    plan_names = [f"{plan[1]} - {plan[2]}" for plan in planes]
    plan_ids = {f"{plan[1]} - {plan[2]}": plan[0] for plan in planes}  # Mapeo de nombre del plan a plan_id

    return plan_names, plan_ids  # Devolvemos ambas listas

# Crear la ventana principal
root = tk.Tk()
root.title("Inscripción de Alumno")
root.geometry("600x400")  # Establecer tamaño inicial de la ventana
root.resizable(True, True)  # Hacer la ventana redimensionable

# Etiquetas y campos de entrada para los datos del alumno
label_dni = tk.Label(root, text="DNI del Alumno:", font=("Arial", 12))
label_dni.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_dni = tk.Entry(root, font=("Arial", 12))
entry_dni.grid(row=0, column=1, padx=10, pady=5, sticky="w")

label_nombre = tk.Label(root, text="Nombre del Alumno:", font=("Arial", 12))
label_nombre.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_nombre = tk.Entry(root, font=("Arial", 12))
entry_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="w")

label_curso = tk.Label(root, text="Curso del Alumno:", font=("Arial", 12))
label_curso.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_curso = tk.Entry(root, font=("Arial", 12))
entry_curso.grid(row=2, column=1, padx=10, pady=5, sticky="w")

label_plan = tk.Label(root, text="Plan de Convalidación:", font=("Arial", 12))
label_plan.grid(row=3, column=0, padx=10, pady=5, sticky="e")

# Cargar los planes de convalidación desde la base de datos
plan_names, plan_ids = cargar_planes()

# Crear el OptionMenu con los planes obtenidos
plan_combobox = tk.StringVar()
plan_combobox.set('')
plan_menu = tk.OptionMenu(root, plan_combobox, *plan_names)
plan_menu.config(font=("Arial", 12))
plan_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Botón para registrar la inscripción
button_inscribir = tk.Button(root, text="Registrar Inscripción", command=registrar_inscripcion, font=("Arial", 12))
button_inscribir.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
