import tkinter as tk
from tkinter import messagebox
import sqlite3

def obtener_grados():
    """Obtiene los grados desde la base de datos."""
    try:
        conexion = sqlite3.connect("../db/sicue.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT DISTINCT nombre FROM grados")
        grados = [row[0] for row in cursor.fetchall()]
        conexion.close()
        return grados
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al obtener los grados: {e}")
        return []

def obtener_asignaturas(grado):
    """Obtiene las asignaturas asociadas a un grado desde la base de datos."""
    try:
        conexion = sqlite3.connect("../db/sicue.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT asignaturas FROM grados WHERE nombre = ?", (grado,))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado and resultado[0]:
            return resultado[0].split(",")  # Asume que las asignaturas están separadas por comas
        return []
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al obtener las asignaturas: {e}")
        return []

def dni_ya_registrado(dni):
    """Verifica si un DNI ya tiene una inscripción en la base de datos."""
    try:
        conexion = sqlite3.connect("../db/sicue.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM inscripciones_profesores WHERE dni = ?", (dni,))
        resultado = cursor.fetchone()
        conexion.close()

        return resultado[0] > 0  # Si el conteo es mayor que 0, el DNI ya está registrado
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al verificar el DNI: {e}")
        return False

def registrar_inscripcion():
    """Lógica para registrar la inscripción del profesor."""
    dni = entry_dni.get()
    grado = var_grado.get()
    asignaturas = [listbox_asignaturas.get(i) for i in listbox_asignaturas.curselection()]
    duracion = var_duracion.get()

    if not dni or not grado or not asignaturas or not duracion:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    if dni_ya_registrado(dni):
        messagebox.showerror("Error", "Este profesor ya tiene una inscripción registrada.")
        return

    # Registrar en la base de datos
    try:
        conexion = sqlite3.connect("../db/sicue.db")
        cursor = conexion.cursor()

        for asignatura in asignaturas:
            cursor.execute("INSERT INTO inscripciones_profesores (dni, grado, asignatura, duracion) VALUES (?, ?, ?, ?)",
                           (dni, grado, asignatura, duracion))

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Inscripción registrada exitosamente.")
        limpiar_campos()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al registrar la inscripción: {e}")

def limpiar_campos():
    """Limpia los campos de la interfaz."""
    entry_dni.delete(0, tk.END)
    var_grado.set("")
    listbox_asignaturas.delete(0, tk.END)
    var_duracion.set("")

def actualizar_asignaturas(*args):
    """Actualiza la lista de asignaturas según el grado seleccionado."""
    grado = var_grado.get()
    asignaturas = obtener_asignaturas(grado)

    listbox_asignaturas.delete(0, tk.END)
    for asignatura in asignaturas:
        listbox_asignaturas.insert(tk.END, asignatura)

# Crear ventana
root = tk.Tk()
root.title("Inscripción Profesores")
root.geometry("600x400")  # Establecer tamaño inicial de la ventana
root.resizable(True, True)  # Hacer la ventana redimensionable

# Variables
var_grado = tk.StringVar()
var_grado.trace("w", actualizar_asignaturas)  # Actualiza asignaturas cuando cambia el grado
var_duracion = tk.StringVar()

# Etiquetas y campos
label_dni = tk.Label(root, text="DNI del Profesor:", font=("Arial", 12))
label_dni.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_dni = tk.Entry(root, font=("Arial", 12))
entry_dni.grid(row=0, column=1, padx=5, pady=5, sticky="w")

label_grado = tk.Label(root, text="Selecciona tu Grado:", font=("Arial", 12))
label_grado.grid(row=1, column=0, padx=5, pady=5, sticky="e")

# Dropdown para seleccionar grado
opciones_grado = obtener_grados()
dropdown_grado = tk.OptionMenu(root, var_grado, *opciones_grado)
dropdown_grado.config(font=("Arial", 12))
dropdown_grado.grid(row=1, column=1, padx=5, pady=5, sticky="w")

label_asignaturas = tk.Label(root, text="Selecciona las Asignaturas que impartes:", font=("Arial", 12))
label_asignaturas.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Lista de asignaturas (vacía inicialmente)
listbox_asignaturas = tk.Listbox(root, selectmode=tk.MULTIPLE, font=("Arial", 12))
listbox_asignaturas.grid(row=2, column=1, padx=5, pady=5, sticky="w")

label_duracion = tk.Label(root, text="Duración de Participación:", font=("Arial", 12))
label_duracion.grid(row=3, column=0, padx=5, pady=5, sticky="e")

# Radio buttons para la duración
radio_duracion_1 = tk.Radiobutton(root, text="Cuatrimestre", variable=var_duracion, value="Cuatrimestre", font=("Arial", 12))
radio_duracion_1.grid(row=3, column=1, padx=5, pady=5, sticky="w")

radio_duracion_2 = tk.Radiobutton(root, text="Año", variable=var_duracion, value="Año", font=("Arial", 12))
radio_duracion_2.grid(row=4, column=1, padx=5, pady=5, sticky="w")

# Botón para registrar
boton_registrar = tk.Button(root, text="Registrar Inscripción", command=registrar_inscripcion, font=("Arial", 12))
boton_registrar.grid(row=5, column=0, columnspan=2, pady=10)

# Botón para limpiar campos
boton_limpiar = tk.Button(root, text="Limpiar Campos", command=limpiar_campos, font=("Arial", 12))
boton_limpiar.grid(row=6, column=0, columnspan=2, pady=10)

# Configurar el grid para que sea redimensionable
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Iniciar ventana
root.mainloop()
