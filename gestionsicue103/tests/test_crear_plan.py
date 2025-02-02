# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch, MagicMock
from crear_plan import crear_plan_convalidacion

# Mock de la función conectar_db
@patch('crear_plan.conectar_db')
@patch('crear_plan.messagebox')
def test_crear_plan_convalidacion(mock_messagebox, mock_conectar_db):
    # Crear un mock para la conexión y el cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_db.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Configurar los valores de entrada
    universidad_origen = "Universidad A"
    universidad_destino = "Universidad B"
    duracion = "6"
    asignaturas = "Asignatura 1, Asignatura 2"
    asignaturas_convalidadas = "Asignatura 3, Asignatura 4"

    # Mock de los widgets de entrada
    with patch('crear_plan.entry_origen.get', return_value=universidad_origen), \
         patch('crear_plan.entry_destino.get', return_value=universidad_destino), \
         patch('crear_plan.entry_duracion.get', return_value=duracion), \
         patch('crear_plan.entry_asignaturas.get', return_value=asignaturas), \
         patch('crear_plan.entry_asignaturas_convalidadas.get', return_value=asignaturas_convalidadas):

        # Llamar a la función a testear
        crear_plan_convalidacion()

        # Verificar que se ejecutaron las consultas correctas
        mock_cursor.execute.assert_called_once_with("""
            INSERT INTO planes_convalidacion (universidad_origen, universidad_destino, duracion, asignaturas, asignaturas_convalidadas)
            VALUES (?, ?, ?, ?, ?)
        """, (universidad_origen, universidad_destino, duracion, asignaturas, asignaturas_convalidadas))
        mock_conn.commit.assert_called_once()

        # Verificar que se mostró el mensaje de éxito
        mock_messagebox.showinfo.assert_called_once_with("Éxito", "Plan de convalidación creado con éxito.")

        # Verificar que se limpiaron los campos de entrada
        crear_plan.entry_origen.delete.assert_called_once_with(0, tk.END)
        crear_plan.entry_destino.delete.assert_called_once_with(0, tk.END)
        crear_plan.entry_duracion.delete.assert_called_once_with(0, tk.END)
        crear_plan.entry_asignaturas.delete.assert_called_once_with(0, tk.END)
        crear_plan.entry_asignaturas_convalidadas.delete.assert_called_once_with(0, tk.END)

# Mock de la función conectar_db para el caso de campos vacíos
@patch('crear_plan.conectar_db')
@patch('crear_plan.messagebox')
def test_crear_plan_convalidacion_campos_vacios(mock_messagebox, mock_conectar_db):
    # Configurar los valores de entrada vacíos
    universidad_origen = ""
    universidad_destino = ""
    duracion = ""
    asignaturas = ""
    asignaturas_convalidadas = ""

    # Mock de los widgets de entrada
    with patch('crear_plan.entry_origen.get', return_value=universidad_origen), \
         patch('crear_plan.entry_destino.get', return_value=universidad_destino), \
         patch('crear_plan.entry_duracion.get', return_value=duracion), \
         patch('crear_plan.entry_asignaturas.get', return_value=asignaturas), \
         patch('crear_plan.entry_asignaturas_convalidadas.get', return_value=asignaturas_convalidadas):

        # Llamar a la función a testear
        crear_plan_convalidacion()

        # Verificar que se mostró el mensaje de error
        mock_messagebox.showerror.assert_called_once_with("Error", "Por favor, complete todos los campos.")

        # Verificar que no se ejecutaron consultas a la base de datos
        mock_conectar_db.assert_not_called()