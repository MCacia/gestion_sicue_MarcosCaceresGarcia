# -*- coding: utf-8 -*-
# conectar_db.py

import sqlite3
import os

def conectar_db(database_name='sicue.db', timeout=10):
    """
    Establece una conexión con la base de datos SQLite.

    Args:
        database_name (str): Nombre del archivo de la base de datos.
        timeout (int): Tiempo de espera para la conexión (en segundos).

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos.

    Raises:
        sqlite3.Error: En caso de que ocurra un error al conectar a la base de datos.
    """
    try:
        # Obtener la ruta absoluta del archivo de base de datos
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, '..', 'db', database_name)
        conn = sqlite3.connect(db_path, timeout=timeout)
        return conn

    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise
