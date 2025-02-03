import sys
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../', 'utils')))

def registrar():
    """Lógica para registrar un usuario nuevo."""
    tipo_usuario = "Profesor" if var_tipo.get() == 1 else "Alumno"
    nombre = entry_nombre.get()
    identificador = entry_identificador.get()

    if tipo_usuario == "Profesor":
        correo = entry_extra.get()
        grado = entry_extra2.get()
        if not (nombre and identificador and correo and grado):
            messagebox.showerror("Error", "Por favor, rellena todos los campos para registrar un profesor.")
            return

        conexion = sqlite3.connect("../db/sicue.db")
        cursor = conexion.cursor()

        # Comprobar si el DNI ya existe
        cursor.execute("SELECT * FROM profesores WHERE DNI = ?", (identificador,))
        if cursor.fetchone():
            messagebox.showerror("Error", "El DNI ya existe en la base de datos.")
            conexion.close()
            return

        cursor.execute("INSERT INTO profesores (DNI, nombre, correo, grado) VALUES (?, ?, ?, ?)", (identificador, nombre, correo, grado))
        conexion.commit()
        conexion.close()
    else:
        curso = entry_extra.get()
        if not (nombre and identificador and curso):
            messagebox.showerror("Error", "Por favor, rellena todos los campos para registrar un alumno.")
            return

        conexion = sqlite3.connect("../db/sicue.db")
        cursor = conexion.cursor()

        # Comprobar si el DNI ya existe
        cursor.execute("SELECT * FROM estudiantes WHERE dni = ?", (identificador,))
        if cursor.fetchone():
            messagebox.showerror("Error", "El DNI ya existe en la base de datos.")
            conexion.close()
            return

        cursor.execute("INSERT INTO estudiantes (dni, nombre, curso) VALUES (?, ?, ?)", (identificador, nombre, curso))
        conexion.commit()
        conexion.close()

    messagebox.showinfo("Éxito", f"{tipo_usuario} registrado exitosamente.")
    limpiar_campos()

def iniciar_sesion():
    """Lógica para iniciar sesión."""
    tipo_usuario = "Profesor" if var_tipo.get() == 1 else "Alumno"
    identificador = entry_identificador.get()

    if not identificador:
        messagebox.showerror("Error", "Por favor, introduce el identificador.")
        return

    conexion = sqlite3.connect("../db/sicue.db")
    cursor = conexion.cursor()

    if tipo_usuario == "Profesor":
        cursor.execute("SELECT * FROM profesores WHERE DNI = ?", (identificador,))
    else:
        cursor.execute("SELECT * FROM estudiantes WHERE dni = ?", (identificador,))

    usuario = cursor.fetchone()
    conexion.close()

    if usuario:
        # Verificamos si el DNI corresponde al administrador
        if identificador == "31024607E":
            messagebox.showinfo("Bienvenido", "Inicio de sesión exitoso como Administrador.")
            redirigir_menu("Administrador")  # Redirige al menú de administrador
        else:
            messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso como {tipo_usuario}.")
            redirigir_menu(tipo_usuario)  # Redirige al menú de profesor o alumno
    else:
        messagebox.showerror("Error", "Identificador no encontrado.")

def limpiar_campos():
    """Limpia los campos de entrada."""
    entry_nombre.delete(0, tk.END)
    entry_identificador.delete(0, tk.END)
    entry_extra.delete(0, tk.END)
    entry_extra2.delete(0, tk.END)

def cambiar_tipo():
    """Cambia las etiquetas de los campos según el tipo seleccionado."""
    if var_tipo.get() == 1:
        label_extra.config(text="Correo:")
        label_extra2.config(text="Grado:")
        entry_extra2.grid(row=5, column=1, padx=5, pady=5)
    else:
        label_extra.config(text="Curso:")
        label_extra2.grid_remove()
        entry_extra2.grid_remove()

# Función para redirigir al menú de acuerdo al tipo de usuario
def redirigir_menu(tipo_usuario):
    root.withdraw()  # Ocultamos la ventana de inicio de sesión
    menu_window = tk.Toplevel(root)
    menu_window.title(f"Menú Principal - {tipo_usuario}")

    if tipo_usuario == "Administrador":
        # Menú de Administrador con opciones adicionales
        tk.Button(menu_window, text="Crear Planes de Convalidación", command=lambda: ejecutar_app("crear_plan.py")).pack(pady=10)
        tk.Button(menu_window, text="Modificar PLan de Convalidacion", command=lambda: ejecutar_app("modificar_plan.py")).pack(pady=10)
        tk.Button(menu_window, text="Consultar Inscripciones", command=lambda: ejecutar_app("consulta_inscripciones.py")).pack(pady=10)
        tk.Button(menu_window, text="Anular Inscripciones", command=lambda: ejecutar_app("anular_inscripciones.py")).pack(pady=10)
        tk.Button(menu_window, text="Consultar Planes", command=lambda: ejecutar_app("consulta_planes.py")).pack(pady=10)
        tk.Button(menu_window, text="Administrar Grados", command=lambda: ejecutar_app("administrar_asignaturas.py")).pack(pady=10)
        tk.Button(menu_window, text="Aprobad/Denegar Solicitudes", command=lambda: ejecutar_app("estado_solicitud.py")).pack(pady=10)
        tk.Button(menu_window, text="Matricular Alumnos", command=lambda: ejecutar_app("matricular.py")).pack(pady=10)
    elif tipo_usuario == "Profesor":
        # Menú para Profesores
        tk.Button(menu_window, text="Seleccionar Grado y Asignaturas", command=lambda: ejecutar_app("inscripciones_profesores2.py")).pack(pady=10)
        tk.Button(menu_window, text="Consultar Planes", command=lambda: ejecutar_app("consulta_planes.py")).pack(pady=10)
        tk.Button(menu_window, text="Anular Inscripcion", command=lambda: ejecutar_app("anular_inscripciones_profes.py")).pack(pady=10)
    else:
        # Menú para Alumnos
        tk.Button(menu_window, text="Inscribirse en Plan de Convalidación", command=lambda: ejecutar_app("inscripcion.py")).pack(pady=10)
        tk.Button(menu_window, text="Anular Inscripción", command=lambda: ejecutar_app("anular_inscripciones.py")).pack(pady=10)
        tk.Button(menu_window, text="Consultar Planes de Convalidación", command=lambda: ejecutar_app("consulta_planes.py")).pack(pady=10)

    # Botón de salir
    tk.Button(menu_window, text="Salir", command=lambda: salir(menu_window)).pack(pady=10)

def ejecutar_app(script_name):
    """Función para ejecutar otros scripts de la aplicación."""
    try:
        subprocess.run(['python3', script_name], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"No se pudo ejecutar {script_name}: {str(e)}")

def salir(menu_window):
    """Cerrar la ventana del menú y volver a la ventana principal de inicio de sesión."""
    menu_window.destroy()  # Cierra la ventana del menú
    root.deiconify()  # Muestra de nuevo la ventana de inicio de sesión

# Crear ventana principal
root = tk.Tk()
root.title("Gestión SICUE")
root.geometry("400x400")  # Establecer tamaño inicial de la ventana
root.resizable(True, True)  # Hacer la ventana redimensionable

# Variables
var_tipo = tk.IntVar(value=2)

# Widgets
label_titulo = tk.Label(root, text="Gestión SICUE", font=("Arial", 20))
label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

radio_profesor = tk.Radiobutton(root, text="Profesor", variable=var_tipo, value=1, command=cambiar_tipo, font=("Arial", 12))
radio_profesor.grid(row=1, column=0, padx=5, pady=5)

radio_alumno = tk.Radiobutton(root, text="Alumno", variable=var_tipo, value=2, command=cambiar_tipo, font=("Arial", 12))
radio_alumno.grid(row=1, column=1, padx=5, pady=5)

label_nombre = tk.Label(root, text="Nombre:", font=("Arial", 12))
label_nombre.grid(row=2, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(root, font=("Arial", 12))
entry_nombre.grid(row=2, column=1, padx=5, pady=5)

label_identificador = tk.Label(root, text="ID/DNI:", font=("Arial", 12))
label_identificador.grid(row=3, column=0, padx=5, pady=5)
entry_identificador = tk.Entry(root, font=("Arial", 12))
entry_identificador.grid(row=3, column=1, padx=5, pady=5)

label_extra = tk.Label(root, text="Curso:", font=("Arial", 12))
label_extra.grid(row=4, column=0, padx=5, pady=5)
entry_extra = tk.Entry(root, font=("Arial", 12))
entry_extra.grid(row=4, column=1, padx=5, pady=5)

label_extra2 = tk.Label(root, text="Grado:", font=("Arial", 12))
entry_extra2 = tk.Entry(root, font=("Arial", 12))

# Botones
boton_registrar = tk.Button(root, text="Registrar", command=registrar, font=("Arial", 12))
boton_registrar.grid(row=6, column=0, padx=5, pady=10)

boton_iniciar = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion, font=("Arial", 12))
boton_iniciar.grid(row=6, column=1, padx=5, pady=10)

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

# Iniciar bucle de la aplicación
root.mainloop()



