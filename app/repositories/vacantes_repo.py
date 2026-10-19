from app.core.database import Database
from app.models.vacantes import Vacantes


class VacantesRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM vacantes
            ORDER BY id_vacante ASC
        """)

        vacantes = cursor.fetchall()

        cursor.close()
        conn.close()

        return vacantes

    def obtener_por_id(self, id_vacante: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM vacantes
            WHERE id_vacante = %s
        """, (id_vacante,))

        vacante = cursor.fetchone()

        cursor.close()
        conn.close()

        return vacante

    def crear(self, vacante: Vacantes):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO vacantes
            (
                id_empresa,
                titulo,
                descripcion,
                requisitos,
                area,
                cargo,
                modalidad,
                tipo_contrato,
                salario,
                ciudad,
                fecha_publicacion,
                fecha_cierre,
                estado,
                cupos
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING id_vacante
        """, (
            vacante.id_empresa,
            vacante.titulo,
            vacante.descripcion,
            vacante.requisitos,
            vacante.area,
            vacante.cargo,
            vacante.modalidad,
            vacante.tipo_contrato,
            vacante.salario,
            vacante.ciudad,
            vacante.fecha_publicacion,
            vacante.fecha_cierre,
            vacante.estado,
            vacante.cupos
        ))

        nuevo_id = cursor.fetchone()["id_vacante"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(self, id_vacante: int, vacante: Vacantes):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE vacantes
            SET id_empresa = %s,
                titulo = %s,
                descripcion = %s,
                requisitos = %s,
                area = %s,
                cargo = %s,
                modalidad = %s,
                tipo_contrato = %s,
                salario = %s,
                ciudad = %s,
                fecha_publicacion = %s,
                fecha_cierre = %s,
                estado = %s,
                cupos = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_vacante = %s
            RETURNING id_vacante
        """, (
            vacante.id_empresa,
            vacante.titulo,
            vacante.descripcion,
            vacante.requisitos,
            vacante.area,
            vacante.cargo,
            vacante.modalidad,
            vacante.tipo_contrato,
            vacante.salario,
            vacante.ciudad,
            vacante.fecha_publicacion,
            vacante.fecha_cierre,
            vacante.estado,
            vacante.cupos,
            id_vacante
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_vacante: int):
        # Eliminación lógica: la fila NO se borra, solo cambia el estado.

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE vacantes
            SET estado = 'Inactiva',
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_vacante = %s
            RETURNING id_vacante
        """, (id_vacante,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None
