import sqlite3

def generar_reporte_html(nombre_db, archivo_salida="reporte.html"):
    """Genera un reporte HTML con los datos de todas las tablas de la base de datos SQLite."""
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect(nombre_db)
        cursor = conexion.cursor()

        # Obtener todas las tablas de la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tablas = [tabla[0] for tabla in cursor.fetchall()]

        if not tablas:
            print("No se encontraron tablas en la base de datos.")
            return

        print(f"Tablas encontradas: {tablas}")

        # Iniciar la estructura del HTML
        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte de Base de Datos</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Reporte de la Base de Datos</h1>
        """

        # Recorrer cada tabla y obtener sus datos
        for tabla in tablas:
            cursor.execute(f"PRAGMA table_info({tabla})")
            columnas = [col[1] for col in cursor.fetchall()]  # Obtener nombres de columnas
            
            if not columnas:
                print(f"La tabla {tabla} no tiene columnas definidas.")
                continue
            
            cursor.execute(f"SELECT * FROM {tabla}")
            datos = cursor.fetchall()

            if not datos:
                print(f"La tabla {tabla} no tiene datos.")
                continue

            # Construir la tabla en HTML
            html += f"<h2>Tabla: {tabla}</h2>\n<table>\n<tr>\n"
            for columna in columnas:
                html += f"<th>{columna}</th>\n"
            html += "</tr>\n"

            for fila in datos:
                html += "<tr>\n"
                for valor in fila:
                    html += f"<td>{valor}</td>\n"
                html += "</tr>\n"

            html += "</table>\n"

        html += "</body></html>"

        # Guardar el archivo HTML
        with open(archivo_salida, "w", encoding="utf-8") as archivo:
            archivo.write(html)

        print(f"Reporte generado exitosamente: {archivo_salida}")

    except sqlite3.Error as e:
        print(f"Error al generar el reporte: {e}")
    finally:
        if conexion:
            conexion.close()

# Uso del script
generar_reporte_html("../db/sicue.db")  # Asegúrate de que "sicue.db" sea el nombre correcto de tu base de datos
