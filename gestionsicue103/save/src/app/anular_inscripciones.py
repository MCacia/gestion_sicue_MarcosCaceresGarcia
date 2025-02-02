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

from utils.conectar_db import conectar_db  # Importar la función desde el archivo conectar_db.py

# Función para realizar la anulación de inscripciones
def anular_inscripciones():
    dni = entry_dni.get()  # Obtener el DNI del alumno para filtrar la consulta
    if not dni:
        messagebox.showerror("Error", "Por favor, ingrese el DNI del alumno.")
        return

    try:
        # Realizar la anulación en la base de datos
        with conectar_db() as conn:
            c = conn.cursor()

            # Consulta para obtener las inscripciones del alumno
            c.execute("""
                SELECT e.nombre, e.curso, p.universidad_origen, p.universidad_destino, i.fecha_inscripcion
                FROM inscripciones i
                JOIN estudiantes e ON e.dni = i.estudiante_id
                JOIN planes_convalidacion p ON p.id = i.plan_id
                WHERE e.dni = ?
            """, (dni,))
            inscripciones = c.fetchall()

            # Si no se encuentran inscripciones para el alumno
            if not inscripciones:
                messagebox.showinfo("Resultado", "No se encontraron inscripciones para el alumno con DNI: " + dni)
                return

            # Anular las inscripciones del alumno
            c.execute("DELETE FROM inscripciones WHERE estudiante_id = ?", (dni,))
            conn.commit()

        messagebox.showinfo("Éxito", "Inscripciones anuladas con éxito para el alumno con DNI: " + dni)

        # Limpiar la lista de resultados anteriores
        for row in treeview.get_children():
            treeview.delete(row)

        # Agregar los resultados a la vista de la tabla
        for inscripcion in inscripciones:
            treeview.insert("", "end", values=inscripcion)

    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error al anular las inscripciones: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Anulación de Inscripciones")

# Etiqueta y campo de entrada para el DNI del alumno
label_dni = tk.Label(root, text="DNI del Alumno:")
label_dni.grid(row=0, column=0, padx=10, pady=5)
entry_dni = tk.Entry(root)
entry_dni.grid(row=0, column=1, padx=10, pady=5)

# Botón para realizar la anulación
button_anular = tk.Button(root, text="Anular Inscripciones", command=anular_inscripciones)
button_anular.grid(row=1, column=0, columnspan=2, pady=10)

# Crear un Treeview para mostrar los resultados
treeview = ttk.Treeview(root, columns=("Nombre", "Curso", "Universidad Origen", "Universidad Destino", "Fecha Inscripcion"), show="headings")
treeview.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Definir las columnas de la tabla
treeview.heading("Nombre", text="Nombre")
treeview.heading("Curso", text="Curso")
treeview.heading("Universidad Origen", text="Universidad Origen")
treeview.heading("Universidad Destino", text="Universidad Destino")
treeview.heading("Fecha Inscripcion", text="Fecha Inscripción")

# Ajustar el ancho de las columnas
treeview.column("Nombre", width=150)
treeview.column("Curso", width=50)
treeview.column("Universidad Origen", width=150)
treeview.column("Universidad Destino", width=150)
treeview.column("Fecha Inscripcion", width=120)

root.mainloop()
