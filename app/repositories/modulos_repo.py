from app.core.database import Database
from app.models.modulos import Modulos


class ModulosRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM modulos
            ORDER BY id_modulo ASC
        """)

        modulos = cursor.fetchall()

        cursor.close()
        conn.close()

        return modulos

    def obtener_por_id(self, id_modulo: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM modulos
            WHERE id_modulo = %s
        """, (id_modulo,))

        modulo = cursor.fetchone()

        cursor.close()
        conn.close()

        return modulo

    def crear(self, modulo: Modulos):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO modulos
            (nombre, descripcion)
            VALUES (%s, %s)
            RETURNING id_modulo
        """, (
            modulo.nombre,
            modulo.descripcion
        ))

        nuevo_id = cursor.fetchone()["id_modulo"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(self, id_modulo: int, modulo: Modulos):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE modulos
            SET nombre = %s,
                descripcion = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_modulo = %s
            RETURNING id_modulo
        """, (
            modulo.nombre,
            modulo.descripcion,
            id_modulo
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_modulo: int):
        # Eliminación lógica: la fila NO se borra, solo cambia el estado.

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE modulos
            SET estado = FALSE,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_modulo = %s
            RETURNING id_modulo
        """, (id_modulo,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None
