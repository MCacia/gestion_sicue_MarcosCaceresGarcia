import tkinter as tk
from subprocess import Popen
import os
import sys

# Ruta de los scripts
ruta_crear_plan = "./crear_plan.py"
ruta_inscripcion = "./inscripcion.py"
ruta_anular_inscripcion = "./anular_inscripciones.py"

# Función para ejecutar el script de Crear Plan
def ejecutar_crear_plan():
    Popen([sys.executable, ruta_crear_plan], shell=False, env=dict(os.environ, PYTHONPATH=os.path.abspath(os.path.join(os.getcwd(), "src"))))

# Función para ejecutar el script de Inscripción
def ejecutar_inscripcion():
    Popen([sys.executable, ruta_inscripcion], shell=False, env=dict(os.environ, PYTHONPATH=os.path.abspath(os.path.join(os.getcwd(), "src"))))

# Función para ejecutar el script de Anulación de Inscripción
def ejecutar_anular_inscripcion():
    Popen([sys.executable, ruta_anular_inscripcion], shell=False, env=dict(os.environ, PYTHONPATH=os.path.abspath(os.path.join(os.getcwd(), "src"))))

# Crear la ventana principal
root = tk.Tk()
root.title("Menú Principal")

# Botones para abrir los programas
boton_crear_plan = tk.Button(root, text="Crear Plan de Convalidación", command=ejecutar_crear_plan, width=30, pady=10)
boton_crear_plan.pack(pady=10)

boton_inscripcion = tk.Button(root, text="Registrar Inscripción", command=ejecutar_inscripcion, width=30, pady=10)
boton_inscripcion.pack(pady=10)

boton_anular_inscripcion = tk.Button(root, text="Anular Inscripción", command=ejecutar_anular_inscripcion, width=30, pady=10)
boton_anular_inscripcion.pack(pady=10)

# Iniciar la ventana principal
root.mainloop()


