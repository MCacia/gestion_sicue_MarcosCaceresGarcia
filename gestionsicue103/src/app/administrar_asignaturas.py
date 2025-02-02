import tkinter as tk
from tkinter import messagebox
import sqlite3

# Función para conectar a la base de datos
def conectar_db():
    return sqlite3.connect("../db/sicue.db")

# Función para obtener todos los grados disponibles
def obtener_grados():
    """Obtiene los grados desde la base de datos."""
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM grados")
        grados = cursor.fetchall()
        conexion.close()
        return grados
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al obtener los grados: {e}")
        return []

# Función para agregar un nuevo grado
def agregar_grado():
    """Agrega un nuevo grado a la base de datos."""
    nombre_grado = entry_grado.get()
    if not nombre_grado:
        messagebox.showerror("Error", "El nombre del grado no puede estar vacío.")
        return

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO grados (nombre, asignaturas) VALUES (?, ?)", (nombre_grado, ""))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", f"Grado '{nombre_grado}' agregado exitosamente.")
        actualizar_grados()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al agregar el grado: {e}")

# Función para actualizar la lista de grados
def actualizar_grados():
    """Actualiza el dropdown de grados."""
    grados = obtener_grados()
    grados_nombres = [grado[1] for grado in grados]
    
    # Actualizar el menú de grados
    var_grado.set("")  # Limpiar selección actual
    menu_grado['menu'].delete(0, 'end')  # Limpiar las opciones existentes
    for grado in grados_nombres:
        menu_grado['menu'].add_command(label=grado, command=tk._setit(var_grado, grado))
    
    # Actualizar los valores de grados
    global grados_disponibles
    grados_disponibles = {grado[1]: grado[0] for grado in grados}  # Mapa de grado -> id

# Función para agregar asignaturas a un grado
def agregar_asignatura():
    """Agrega una asignatura a un grado seleccionado."""
    grado_nombre = var_grado.get()
    asignatura = entry_asignatura.get()
    
    if not grado_nombre or not asignatura:
        messagebox.showerror("Error", "Debe seleccionar un grado y escribir una asignatura.")
        return
    
    grado_id = grados_disponibles.get(grado_nombre)
    if not grado_id:
        messagebox.showerror("Error", "El grado seleccionado no es válido.")
        return
    
    try:
        # Obtener asignaturas actuales
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT asignaturas FROM grados WHERE id = ?", (grado_id,))
        resultado = cursor.fetchone()
        if resultado:
            asignaturas_actuales = resultado[0]
            nuevas_asignaturas = f"{asignaturas_actuales},{asignatura}" if asignaturas_actuales else asignatura
            cursor.execute("UPDATE grados SET asignaturas = ? WHERE id = ?", (nuevas_asignaturas, grado_id))
            conexion.commit()
            conexion.close()
            
            messagebox.showinfo("Éxito", f"Asinatura '{asignatura}' añadida al grado '{grado_nombre}'.")
            entry_asignatura.delete(0, tk.END)  # Limpiar campo de asignatura
            actualizar_grados()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al agregar la asignatura: {e}")

# Función para eliminar asignaturas de un grado
def eliminar_asignatura():
    """Elimina una asignatura de un grado seleccionado."""
    grado_nombre = var_grado.get()
    asignatura = entry_asignatura.get()
    
    if not grado_nombre or not asignatura:
        messagebox.showerror("Error", "Debe seleccionar un grado y escribir una asignatura.")
        return
    
    grado_id = grados_disponibles.get(grado_nombre)
    if not grado_id:
        messagebox.showerror("Error", "El grado seleccionado no es válido.")
        return
    
    try:
        # Obtener asignaturas actuales
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT asignaturas FROM grados WHERE id = ?", (grado_id,))
        resultado = cursor.fetchone()
        if resultado:
            asignaturas_actuales = resultado[0]
            asignaturas_list = asignaturas_actuales.split(",")
            if asignatura in asignaturas_list:
                asignaturas_list.remove(asignatura)
                nuevas_asignaturas = ",".join(asignaturas_list)
                cursor.execute("UPDATE grados SET asignaturas = ? WHERE id = ?", (nuevas_asignaturas, grado_id))
                conexion.commit()
                conexion.close()
                
                messagebox.showinfo("Éxito", f"Asinatura '{asignatura}' eliminada del grado '{grado_nombre}'.")
                entry_asignatura.delete(0, tk.END)  # Limpiar campo de asignatura
                actualizar_grados()
            else:
                messagebox.showerror("Error", f"La asignatura '{asignatura}' no se encuentra en el grado '{grado_nombre}'.")
    
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Hubo un error al eliminar la asignatura: {e}")

# Crear ventana
root = tk.Tk()
root.title("Gestión de Grados y Asignaturas")
root.geometry("500x400")  # Establecer tamaño inicial de la ventana
root.resizable(True, True)  # Hacer la ventana redimensionable

# Variables
var_grado = tk.StringVar()
grados_disponibles = {}

# Etiquetas y campos
label_grado = tk.Label(root, text="Selecciona el Grado:", font=("Arial", 12))
label_grado.grid(row=0, column=0, padx=5, pady=5, sticky="e")

menu_grado = tk.OptionMenu(root, var_grado, "")
menu_grado.config(font=("Arial", 12))
menu_grado.grid(row=0, column=1, padx=5, pady=5, sticky="w")

label_grado_nombre = tk.Label(root, text="Nombre del Nuevo Grado:", font=("Arial", 12))
label_grado_nombre.grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_grado = tk.Entry(root, font=("Arial", 12))
entry_grado.grid(row=1, column=1, padx=5, pady=5, sticky="w")

boton_agregar_grado = tk.Button(root, text="Agregar Grado", command=agregar_grado, font=("Arial", 12))
boton_agregar_grado.grid(row=2, column=0, columnspan=2, pady=10)

label_asignatura = tk.Label(root, text="Nombre de la Asignatura:", font=("Arial", 12))
label_asignatura.grid(row=4, column=0, padx=5, pady=5, sticky="e")

entry_asignatura = tk.Entry(root, font=("Arial", 12))
entry_asignatura.grid(row=4, column=1, padx=5, pady=5, sticky="w")

boton_agregar_asignatura = tk.Button(root, text="Agregar Asignatura", command=agregar_asignatura, font=("Arial", 12))
boton_agregar_asignatura.grid(row=5, column=0, columnspan=2, pady=10)

boton_eliminar_asignatura = tk.Button(root, text="Eliminar Asignatura", command=eliminar_asignatura, font=("Arial", 12))
boton_eliminar_asignatura.grid(row=6, column=0, columnspan=2, pady=10)

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

# Inicializar grados
actualizar_grados()

# Iniciar ventana
root.mainloop()
