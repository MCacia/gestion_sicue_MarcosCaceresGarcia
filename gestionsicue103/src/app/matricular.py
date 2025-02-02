import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# Establece la conexión a la base de datos
conn = sqlite3.connect('../db/sicue.db')
cursor = conn.cursor()

# Función para obtener las universidades de destino
def obtener_universidades_destino():
    query = '''
    SELECT DISTINCT universidad_destino
    FROM planes_convalidacion
    '''
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

# Función para obtener estudiantes con inscripciones aprobadas, filtrando por universidad
def obtener_estudiantes_aceptados(universidad_destino=None):
    query = '''
    SELECT e.nombre, e.dni, i.fecha_inscripcion, p.universidad_destino, i.plan_id
    FROM estudiantes e
    JOIN inscripciones i ON e.dni = i.estudiante_id
    JOIN planes_convalidacion p ON i.plan_id = p.id
    WHERE i.estado = 'Aprobado'
    '''
    if universidad_destino:
        query += " AND p.universidad_destino = ?"
        cursor.execute(query, (universidad_destino,))
    else:
        cursor.execute(query)
    return cursor.fetchall()

# Función para verificar si el estudiante ya está matriculado
def esta_matriculado(dni, plan_id):
    query = '''
    SELECT 1
    FROM matriculados
    WHERE estudiante_dni = ? AND plan_id = ?
    '''
    cursor.execute(query, (dni, plan_id))
    return cursor.fetchone() is not None

# Función para matricular al estudiante en la universidad de destino
def matricular_estudiante(dni, universidad_destino, plan_id):
    # Verificar si el estudiante ya está matriculado
    if esta_matriculado(dni, plan_id):
        messagebox.showwarning("Error", "Este estudiante ya está matriculado en este plan.")
        return

    # Obtener la fecha de matriculación actual
    fecha_matriculacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertar el estudiante en la tabla "matriculados"
    cursor.execute('''
    INSERT INTO matriculados (estudiante_dni, universidad_destino, fecha_matricula, plan_id)
    VALUES (?, ?, ?, ?)
    ''', (dni, universidad_destino, fecha_matriculacion, plan_id))

    # Guardar los cambios en la base de datos
    conn.commit()

    messagebox.showinfo("Matriculación", f"Estudiante {dni} matriculado en {universidad_destino} con el plan {plan_id}")

    # Actualizar la tabla Treeview después de la matriculación
    actualizar_tabla(universidad_var.get())  # Pasar la universidad seleccionada

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Listado de Estudiantes Aceptados")
root.geometry("600x450")  # Aumentamos un poco el alto

# Widget para seleccionar la universidad de destino
universidades = obtener_universidades_destino()
universidad_var = tk.StringVar(root)
universidad_dropdown = ttk.Combobox(root, textvariable=universidad_var, values=universidades)
universidad_dropdown.current(0)  # Seleccionar la primera universidad por defecto
universidad_dropdown.pack(pady=(10, 0))  # Espacio arriba

# Función para actualizar la tabla al cambiar la universidad
def cambiar_universidad(*args):
    universidad_seleccionada = universidad_var.get()
    actualizar_tabla(universidad_seleccionada)

universidad_var.trace_add("write", cambiar_universidad)  # Llamar a la función al cambiar la selección

# Crear un Treeview para mostrar los estudiantes
tree = ttk.Treeview(root, columns=("Nombre", "DNI", "Fecha Inscripción", "Universidad Destino"), show="headings")
tree.heading("Nombre", text="Nombre")
tree.heading("DNI", text="DNI")
tree.heading("Fecha Inscripción", text="Fecha Inscripción")
tree.heading("Universidad Destino", text="Universidad Destino")

# Función para actualizar la tabla Treeview
def actualizar_tabla(universidad_destino=None):
    tree.delete(*tree.get_children())  # Limpiar la tabla
    for estudiante in obtener_estudiantes_aceptados(universidad_destino):
        tree.insert("", "end", values=estudiante[:4])

tree.pack(pady=10) # Espacio entre el dropdown y la tabla

# Botón para matricular al estudiante seleccionado
def matricular():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Seleccionar Estudiante", "Por favor selecciona un estudiante.")
        return

    estudiante = tree.item(selected_item, "values")
    dni = estudiante[1]
    universidad_destino = estudiante[3]

    # Obtener el plan_id.  Se asegura que el índice corresponda al elemento seleccionado.
    index = tree.index(selected_item)
    plan_id = obtener_estudiantes_aceptados(universidad_var.get())[index][4]

    matricular_estudiante(dni, universidad_destino, plan_id)

matricular_button = tk.Button(root, text="Matricular", command=matricular)
matricular_button.pack(pady=10)

# Mostrar los datos de los estudiantes en el Treeview (inicialmente, sin filtro)
actualizar_tabla()

# Ejecutar la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos cuando la aplicación se cierra
conn.close()
