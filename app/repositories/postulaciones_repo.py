from app.core.database import Database
from app.models.postulaciones import Postulaciones


class PostulacionesRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM postulaciones
            ORDER BY id_postulacion ASC
        """)

        postulaciones = cursor.fetchall()

        cursor.close()
        conn.close()

        return postulaciones

    def obtener_por_id(self, id_postulacion: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM postulaciones
            WHERE id_postulacion = %s
        """, (id_postulacion,))

        postulacion = cursor.fetchone()

        cursor.close()
        conn.close()

        return postulacion

    def crear(self, postulacion: Postulaciones):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO postulaciones
            (
                id_egresado,
                id_vacante,
                estado,
                comentarios
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id_postulacion
        """, (
            postulacion.id_egresado,
            postulacion.id_vacante,
            postulacion.estado,
            postulacion.comentarios
        ))

        nuevo_id = cursor.fetchone()["id_postulacion"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(
        self,
        id_postulacion: int,
        postulacion: Postulaciones
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE postulaciones
            SET id_egresado = %s,
                id_vacante = %s,
                estado = %s,
                comentarios = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_postulacion = %s
            RETURNING id_postulacion
        """, (
            postulacion.id_egresado,
            postulacion.id_vacante,
            postulacion.estado,
            postulacion.comentarios,
            id_postulacion
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_postulacion: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM postulaciones
            WHERE id_postulacion = %s
            RETURNING id_postulacion
        """, (id_postulacion,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None