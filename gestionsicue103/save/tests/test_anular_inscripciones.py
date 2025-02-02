import pytest
from unittest.mock import patch, MagicMock
import tkinter as tk
import sys
import os

# Asegurarse de que el directorio raíz del proyecto esté en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'app')))

from anular_inscripciones import anular_inscripciones, conectar_db

@pytest.fixture
def setup_tkinter():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    entry_dni = tk.Entry(root)
    entry_dni.insert(0, "12345678A")  # Insertar un DNI válido
    treeview = tk.ttk.Treeview(root, columns=("Nombre", "Curso", "Universidad Origen", "Universidad Destino", "Fecha Inscripcion"), show="headings")
    return root, entry_dni, treeview

@patch('anular_inscripciones.conectar_db')
def test_anular_inscripciones(mock_conectar_db, setup_tkinter):
    root, entry_dni, treeview = setup_tkinter

    # Configurar el mock de la base de datos
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Configurar el resultado de la consulta
    mock_cursor.fetchall.return_value = [
        ("Juan Pérez", "2º", "Universidad A", "Universidad B", "2023-01-01")
    ]

    # Llamar a la función anular_inscripciones
    anular_inscripciones()

    # Verificar que se realizó la consulta correcta
    mock_cursor.execute.assert_any_call("""
        SELECT e.nombre, e.curso, p.universidad_origen, p.universidad_destino, i.fecha_inscripcion
        FROM inscripciones i
        JOIN estudiantes e ON e.dni = i.estudiante_id
        JOIN planes_convalidacion p ON p.id = i.plan_id
        WHERE e.dni = ?
    """, ("12345678A",))

    # Verificar que se realizó la anulación correcta
    mock_cursor.execute.assert_any_call("DELETE FROM inscripciones WHERE estudiante_id = ?", ("12345678A",))

    # Verificar que se realizó el commit
    mock_conn.commit.assert_called_once()

    # Verificar que se limpiaron los resultados anteriores
    assert len(treeview.get_children()) == 0

    # Verificar que se agregaron los resultados a la vista de la tabla
    assert len(treeview.get_children()) == 1
    assert treeview.item(treeview.get_children()[0])['values'] == ("Juan Pérez", "2º", "Universidad A", "Universidad B", "2023-01-01")

    # Cerrar la ventana de Tkinter
    root.destroy()


