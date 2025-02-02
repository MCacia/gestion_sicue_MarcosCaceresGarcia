import unittest
from unittest.mock import patch, MagicMock
import crear_plan

class TestCrearPlan(unittest.TestCase):

    @patch('crear_plan.sqlite3.connect')
    def test_conectar_db(self, mock_connect):
        # Simular la conexión a la base de datos
        mock_connect.return_value = MagicMock()
        conn = crear_plan.conectar_db()
        mock_connect.assert_called_once_with('sicue.db', timeout=10)
        self.assertIsNotNone(conn)

    @patch('crear_plan.messagebox.showerror')
    @patch('crear_plan.conectar_db')
    @patch('crear_plan.tk.Entry.get')
    def test_crear_plan_convalidacion_campos_vacios(self, mock_get, mock_conectar_db, mock_showerror):
        # Simular campos vacíos
        mock_get.side_effect = ['', '', '', '', '']
        crear_plan.crear_plan_convalidacion()
        mock_showerror.assert_called_once_with("Error", "Por favor, complete todos los campos.")
        mock_conectar_db.assert_not_called()

    @patch('crear_plan.messagebox.showinfo')
    @patch('crear_plan.conectar_db')
    @patch('crear_plan.tk.Entry.get')
    def test_crear_plan_convalidacion_exito(self, mock_get, mock_conectar_db, mock_showinfo):
        # Simular campos llenos
        mock_get.side_effect = ['Universidad A', 'Universidad B', '6', 'Asignatura 1, Asignatura 2', 'Asignatura 3, Asignatura 4']
        mock_conn = MagicMock()
        mock_conectar_db.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        crear_plan.crear_plan_convalidacion()

        mock_cursor.execute.assert_called_once_with("""
            INSERT INTO planes_convalidacion (universidad_origen, universidad_destino, duracion, asignaturas, asignaturas_convalidadas)
            VALUES (?, ?, ?, ?, ?)
        """, ('Universidad A', 'Universidad B', '6', 'Asignatura 1, Asignatura 2', 'Asignatura 3, Asignatura 4'))
        mock_conn.commit.assert_called_once()
        mock_showinfo.assert_called_once_with("Éxito", "Plan de convalidación creado con éxito.")

if __name__ == '__main__':
    unittest.main()