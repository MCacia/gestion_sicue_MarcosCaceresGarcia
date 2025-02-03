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

def obtener_inscripciones(dni):
    """Obtiene las inscripciones de un profesor desde la base de datos."""
    try:
        conexion = sqlite3.connect("../db/sicue.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, grado, asignatura FROM inscripciones_profesores WHERE dni = ?", (dni,))
        inscripciones = cursor.fetchall()
        conexion.close()
        return inscripciones
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al obtener las inscripciones: {e}")
        return []

def anular_inscripcion():
    """Lógica para anular una inscripción del profesor."""
    dni = entry_dni.get()
    seleccion = listbox_inscripciones.curselection()
    
    if not dni or not seleccion:
        messagebox.showerror("Error", "Por favor, completa todos los campos y selecciona una inscripción.")
        return
    
    inscripcion_id = listbox_inscripciones.get(seleccion[0]).split(" - ")[0]  # Obtener el ID de la inscripción
    
    try:
        conexion = sqlite3.connect("../db/sicue.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM inscripciones_profesores WHERE id = ?", (inscripcion_id,))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Inscripción anulada exitosamente.")
        actualizar_inscripciones()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al anular la inscripción: {e}")

def actualizar_inscripciones():
    """Actualiza la lista de inscripciones según el DNI ingresado."""
    dni = entry_dni.get()
    inscripciones = obtener_inscripciones(dni)
    listbox_inscripciones.delete(0, tk.END)
    for inscripcion in inscripciones:
        listbox_inscripciones.insert(tk.END, f"{inscripcion[0]} - {inscripcion[1]} - {inscripcion[2]}")

# Crear ventana
root = tk.Tk()
root.title("Anulación de Inscripción de Profesores")
root.geometry("600x400")  # Establecer tamaño inicial de la ventana
root.resizable(True, True)  # Hacer la ventana redimensionable

# Etiquetas y campos
label_dni = tk.Label(root, text="DNI del Profesor:", font=("Arial", 12))
label_dni.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_dni = tk.Entry(root, font=("Arial", 12))
entry_dni.grid(row=0, column=1, padx=5, pady=5, sticky="w")

boton_actualizar = tk.Button(root, text="Buscar Inscripciones", command=actualizar_inscripciones, font=("Arial", 12))
boton_actualizar.grid(row=1, column=0, columnspan=2, pady=5)

label_inscripciones = tk.Label(root, text="Selecciona la Inscripción a Anular:", font=("Arial", 12))
label_inscripciones.grid(row=2, column=0, padx=5, pady=5, sticky="e")

listbox_inscripciones = tk.Listbox(root, selectmode=tk.SINGLE, font=("Arial", 12))
listbox_inscripciones.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Botón para anular inscripción
boton_anular = tk.Button(root, text="Anular Inscripción", command=anular_inscripcion, font=("Arial", 12))
boton_anular.grid(row=3, column=0, columnspan=2, pady=10)

# Configurar el grid para que sea redimensionable
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Iniciar ventana
root.mainloop()
