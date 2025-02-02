# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch, MagicMock
from logica_inscripcion import registrar_inscripcion_logic, validar_dni

def test_validar_dni():
    assert validar_dni("12345678A") == True
    assert validar_dni("12345678") == False
    assert validar_dni("1234567A") == False
    assert validar_dni("12345678AA") == False

# Mock de la función conectar_db
@patch('logica_inscripcion.conectar_db')
def test_registrar_inscripcion(mock_conectar_db):
    # Crear un mock para la conexión y el cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_db.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Configurar los valores de entrada
    dni = "12345678A"
    nombre = "Nombre"
    curso = "2º"
    plan_id = 1

    # Llamar a la función a testear
    estado, mensaje = registrar_inscripcion_logic(dni, nombre, curso, plan_id, mock_conectar_db)

    # Verificar que se ejecutaron las consultas correctas
    mock_cursor.execute.assert_any_call("SELECT * FROM inscripciones WHERE estudiante_id = ? AND plan_id = ?", (dni, plan_id))
    mock_cursor.execute.assert_any_call("SELECT * FROM estudiantes WHERE dni=?", (dni,))
    mock_cursor.execute.assert_any_call("INSERT INTO estudiantes (dni, nombre, curso) VALUES (?, ?, ?)", (dni, nombre, curso))
    mock_cursor.execute.assert_any_call("""
        INSERT INTO inscripciones (estudiante_id, plan_id, fecha_inscripcion)
        VALUES (?, ?, datetime('now'))
    """, (dni, plan_id))
    mock_conn.commit.assert_called()

    # Verificar el estado y el mensaje
    assert estado == "Éxito"
    assert mensaje == "Inscripción realizada con éxito."

# Mock de la función conectar_db para el caso de campos vacíos
@patch('logica_inscripcion.conectar_db')
def test_registrar_inscripcion_campos_vacios(mock_conectar_db):
    # Configurar los valores de entrada vacíos
    dni = ""
    nombre = ""
    curso = ""
    plan_id = None

    # Llamar a la función a testear
    estado, mensaje = registrar_inscripcion_logic(dni, nombre, curso, plan_id, mock_conectar_db)

    # Verificar el estado y el mensaje
    assert estado == "Error"
    assert mensaje == "Por favor, complete todos los campos."

    # Verificar que no se ejecutaron consultas a la base de datos
    mock_conectar_db.assert_not_called()

# Mock de la función conectar_db para el caso de DNI inválido
@patch('logica_inscripcion.conectar_db')
def test_registrar_inscripcion_dni_invalido(mock_conectar_db):
    # Configurar los valores de entrada
    dni = "12345678"
    nombre = "Nombre"
    curso = "2º"
    plan_id = 1

    # Llamar a la función a testear
    estado, mensaje = registrar_inscripcion_logic(dni, nombre, curso, plan_id, mock_conectar_db)

    # Verificar el estado y el mensaje
    assert estado == "Error"
    assert mensaje == "El formato del DNI no es válido. Debe tener 8 dígitos seguidos de una letra."

    # Verificar que no se ejecutaron consultas a la base de datos
    mock_conectar_db.assert_not_called()

# Mock de la función conectar_db para el caso de alumno ya inscrito
@patch('logica_inscripcion.conectar_db')
def test_registrar_inscripcion_alumno_ya_inscrito(mock_conectar_db):
    # Crear un mock para la conexión y el cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_db.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Configurar los valores de entrada
    dni = "12345678A"
    nombre = "Nombre"
    curso = "2º"
    plan_id = 1

    # Configurar el resultado de la consulta
    mock_cursor.fetchone.side_effect = [(1,), None]

    # Llamar a la función a testear
    estado, mensaje = registrar_inscripcion_logic(dni, nombre, curso, plan_id, mock_conectar_db)

    # Verificar el estado y el mensaje
    assert estado == "Error"
    assert mensaje == "Este alumno ya está inscrito en este plan de convalidación."

    # Verificar que no se ejecutaron consultas de inserción
    mock_cursor.execute.assert_not_called_with("INSERT INTO estudiantes (dni, nombre, curso) VALUES (?, ?, ?)", (dni, nombre, curso))
    mock_cursor.execute.assert_not_called_with("""
        INSERT INTO inscripciones (estudiante_id, plan_id, fecha_inscripcion)
        VALUES (?, ?, datetime('now'))
    """, (dni, plan_id))
    mock_conn.commit.assert_not_called()

# Mock de la función conectar_db para el caso de DNI ya existente
@patch('logica_inscripcion.conectar_db')
def test_registrar_inscripcion_dni_existente(mock_conectar_db):
    # Crear un mock para la conexión y el cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_db.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Configurar los valores de entrada
    dni = "12345678A"
    nombre = "Nombre"
    curso = "2º"
    plan_id = 1

    # Configurar el resultado de la consulta
    mock_cursor.fetchone.side_effect = [None, (1,)]

    # Llamar a la función a testear
    estado, mensaje = registrar_inscripcion_logic(dni, nombre, curso, plan_id, mock_conectar_db)

    # Verificar el estado y el mensaje
    assert estado == "Error"
    assert mensaje == "El DNI ya existe en la base de datos."

    # Verificar que no se ejecutaron consultas de inserción
    mock_cursor.execute.assert_not_called_with("INSERT INTO estudiantes (dni, nombre, curso) VALUES (?, ?, ?)", (dni, nombre, curso))
    mock_cursor.execute.assert_not_called_with("""
        INSERT INTO inscripciones (estudiante_id, plan_id, fecha_inscripcion)
        VALUES (?, ?, datetime('now'))
    """, (dni, plan_id))
    mock_conn.commit.assert_not_called()

# Mock de la función conectar_db para el caso de curso inválido
@patch('logica_inscripcion.conectar_db')
def test_registrar_inscripcion_curso_invalido(mock_conectar_db):
    # Crear un mock para la conexión y el cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_db.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Configurar los valores de entrada
    dni = "12345678A"
    nombre = "Nombre"
    curso = "1º"
    plan_id = 1

    # Llamar a la función a testear
    estado, mensaje = registrar_inscripcion_logic(dni, nombre, curso, plan_id, mock_conectar_db)

    # Verificar el estado y el mensaje
    assert estado == "Error"
    assert mensaje == "Solo se puede inscribir alumnos de 2º o 3º."

    # Verificar que no se ejecutaron consultas de inserción
    mock_cursor.execute.assert_not_called_with("""
        INSERT INTO inscripciones (estudiante_id, plan_id, fecha_inscripcion)
        VALUES (?, ?, datetime('now'))
    """, (dni, plan_id))
    mock_conn.commit.assert_not_called()