import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# Establece la conexión a la base de datos
conn = sqlite3.connect('../db/sicue.db')
cursor = conn.cursor()

# Función para obtener estudiantes con inscripciones aprobadas
def obtener_estudiantes_aceptados():
    query = '''
    SELECT e.nombre, e.dni, i.fecha_inscripcion, p.universidad_destino, i.plan_id
    FROM estudiantes e
    JOIN inscripciones i ON e.dni = i.estudiante_id
    JOIN planes_convalidacion p ON i.plan_id = p.id
    WHERE i.estado = 'Aprobado'  -- Filtramos por las inscripciones aprobadas
    '''
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

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Listado de Estudiantes Aceptados")
root.geometry("600x400")

# Crear un Treeview para mostrar los estudiantes
tree = ttk.Treeview(root, columns=("Nombre", "DNI", "Fecha Inscripción", "Universidad Destino"), show="headings")
tree.heading("Nombre", text="Nombre")
tree.heading("DNI", text="DNI")
tree.heading("Fecha Inscripción", text="Fecha Inscripción")
tree.heading("Universidad Destino", text="Universidad Destino")

# Mostrar los datos de los estudiantes en el Treeview
for estudiante in obtener_estudiantes_aceptados():
    tree.insert("", "end", values=estudiante[:4])  # Excluimos el plan_id de la visualización

tree.pack(pady=20)

# Función para el botón "Matricular"
def matricular():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Seleccionar Estudiante", "Por favor selecciona un estudiante.")
        return
    
    estudiante = tree.item(selected_item, "values")
    dni = estudiante[1]
    universidad_destino = estudiante[3]
    plan_id = obtener_estudiantes_aceptados()[tree.index(selected_item)][4]  # Obtener el plan_id del estudiante seleccionado
    
    matricular_estudiante(dni, universidad_destino, plan_id)

# Botón para matricular al estudiante seleccionado
matricular_button = tk.Button(root, text="Matricular", command=matricular)
matricular_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos cuando la aplicación se cierra
conn.close()
