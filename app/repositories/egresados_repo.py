from app.core.database import Database
from app.models.egresados import Egresados


class EgresadosRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM egresados
            ORDER BY id_egresado ASC
        """)

        egresados = cursor.fetchall()

        cursor.close()
        conn.close()

        return egresados

    def obtener_por_id(self, id_egresado: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM egresados
            WHERE id_egresado = %s
        """, (id_egresado,))

        egresado = cursor.fetchone()

        cursor.close()
        conn.close()

        return egresado

    def crear(self, egresado: Egresados):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO egresados
            (
                id_usuario,
                codigo_estudiante,
                programa_academico,
                facultad,
                fecha_graduacion,
                nivel_formacion,
                anio_graduacion,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_egresado
        """, (
            egresado.id_usuario,
            egresado.codigo_estudiante,
            egresado.programa_academico,
            egresado.facultad,
            egresado.fecha_graduacion,
            egresado.nivel_formacion,
            egresado.anio_graduacion,
            egresado.estado
        ))

        nuevo_id = cursor.fetchone()["id_egresado"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(self, id_egresado: int, egresado: Egresados):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE egresados
            SET id_usuario = %s,
                codigo_estudiante = %s,
                programa_academico = %s,
                facultad = %s,
                fecha_graduacion = %s,
                nivel_formacion = %s,
                anio_graduacion = %s,
                estado = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_egresado = %s
            RETURNING id_egresado
        """, (
            egresado.id_usuario,
            egresado.codigo_estudiante,
            egresado.programa_academico,
            egresado.facultad,
            egresado.fecha_graduacion,
            egresado.nivel_formacion,
            egresado.anio_graduacion,
            egresado.estado,
            id_egresado
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_egresado: int):
        # Eliminación lógica: la fila NO se borra, solo cambia el estado.

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE egresados
            SET estado = FALSE,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_egresado = %s
            RETURNING id_egresado
        """, (id_egresado,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None
