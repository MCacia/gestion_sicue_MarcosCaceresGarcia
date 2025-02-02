import sys
import os

# Agregar la ruta de la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.conectar_db import conectar_db  # Importar la función modularizada
