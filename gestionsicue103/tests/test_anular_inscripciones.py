# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch, MagicMock
from logica_anular_inscripciones import anular_inscripciones_logic

# Mock de la función conectar_db
@patch('logica_anular_inscripciones.conectar_db')
def test_anular_inscripciones(mock_conectar_db):
    # Crear un mock para la conexión y el cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_db.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Configurar los valores de entrada
    dni = "12345678A"

    # Configurar el resultado de la consulta
    inscripciones = [("Nombre", "Curso", "Universidad Origen", "Universidad Destino", "Fecha Inscripcion")]
    mock_cursor.fetchall.return_value = inscripciones

    # Llamar a la función a testear
    estado, mensaje, resultado = anular_inscripciones_logic(dni, mock_conectar_db)

    # Verificar que se ejecutaron las consultas correctas
    mock_cursor.execute.assert_any_call("""
        SELECT e.nombre, e.curso, p.universidad_origen, p.universidad_destino, i.fecha_inscripcion
        FROM inscripciones i
        JOIN estudiantes e ON e.dni = i.estudiante_id
        JOIN planes_convalidacion p ON p.id = i.plan_id
        WHERE e.dni = ?
    """, (dni,))
    mock_cursor.execute.assert_any_call("DELETE FROM inscripciones WHERE estudiante_id = ?", (dni,))
    mock_conn.commit.assert_called_once()

    # Verificar el estado y el mensaje
    assert estado == "Éxito"
    assert mensaje == "Inscripciones anuladas con éxito para el alumno con DNI: " + dni
    assert resultado == inscripciones

# Mock de la función conectar_db para el caso de DNI vacío
@patch('logica_anular_inscripciones.conectar_db')
def test_anular_inscripciones_dni_vacio(mock_conectar_db):
    # Configurar los valores de entrada vacíos
    dni = ""

    # Llamar a la función a testear
    estado, mensaje, resultado = anular_inscripciones_logic(dni, mock_conectar_db)

    # Verificar el estado y el mensaje
    assert estado == "Error"
    assert mensaje == "Por favor, ingrese el DNI del alumno."
    assert resultado == []

    # Verificar que no se ejecutaron consultas a la base de datos
    mock_conectar_db.assert_not_called()

# Mock de la función conectar_db para el caso de no encontrar inscripciones
@patch('logica_anular_inscripciones.conectar_db')
def test_anular_inscripciones_no_encontradas(mock_conectar_db):
    # Crear un mock para la conexión y el cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_db.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Configurar los valores de entrada
    dni = "12345678A"

    # Configurar el resultado de la consulta
    mock_cursor.fetchall.return_value = []

    # Llamar a la función a testear
    estado, mensaje, resultado = anular_inscripciones_logic(dni, mock_conectar_db)

    # Verificar que se ejecutaron las consultas correctas
    mock_cursor.execute.assert_called_once_with("""
        SELECT e.nombre, e.curso, p.universidad_origen, p.universidad_destino, i.fecha_inscripcion
        FROM inscripciones i
        JOIN estudiantes e ON e.dni = i.estudiante_id
        JOIN planes_convalidacion p ON p.id = i.plan_id
        WHERE e.dni = ?
    """, (dni,))

    # Verificar el estado y el mensaje
    assert estado == "Resultado"
    assert mensaje == "No se encontraron inscripciones para el alumno con DNI: " + dni
    assert resultado == []

    # Verificar que no se ejecutaron consultas de eliminación
    mock_cursor.execute.assert_not_called_with("DELETE FROM inscripciones WHERE estudiante_id = ?", (dni,))
    mock_conn.commit.assert_not_called()
