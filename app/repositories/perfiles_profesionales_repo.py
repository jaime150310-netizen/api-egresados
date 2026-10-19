from app.core.database import Database
from app.models.perfiles_profesionales import PerfilesProfesionales


class PerfilesProfesionalesRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM perfiles_profesionales
            ORDER BY id_perfil ASC
        """)

        perfiles = cursor.fetchall()

        cursor.close()
        conn.close()

        return perfiles

    def obtener_por_id(self, id_perfil: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM perfiles_profesionales
            WHERE id_perfil = %s
        """, (id_perfil,))

        perfil = cursor.fetchone()

        cursor.close()
        conn.close()

        return perfil

    def crear(self, perfil: PerfilesProfesionales):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO perfiles_profesionales
            (
                id_egresado,
                perfil_profesional,
                cargo_deseado,
                area_interes,
                experiencia_anios,
                habilidades,
                idiomas,
                hoja_vida_url,
                linkedin_url,
                portafolio_url,
                disponibilidad
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            RETURNING id_perfil
        """, (
            perfil.id_egresado,
            perfil.perfil_profesional,
            perfil.cargo_deseado,
            perfil.area_interes,
            perfil.experiencia_anios,
            perfil.habilidades,
            perfil.idiomas,
            perfil.hoja_vida_url,
            perfil.linkedin_url,
            perfil.portafolio_url,
            perfil.disponibilidad
        ))

        nuevo_id = cursor.fetchone()["id_perfil"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(
        self,
        id_perfil: int,
        perfil: PerfilesProfesionales
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE perfiles_profesionales
            SET id_egresado = %s,
                perfil_profesional = %s,
                cargo_deseado = %s,
                area_interes = %s,
                experiencia_anios = %s,
                habilidades = %s,
                idiomas = %s,
                hoja_vida_url = %s,
                linkedin_url = %s,
                portafolio_url = %s,
                disponibilidad = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_perfil = %s
            RETURNING id_perfil
        """, (
            perfil.id_egresado,
            perfil.perfil_profesional,
            perfil.cargo_deseado,
            perfil.area_interes,
            perfil.experiencia_anios,
            perfil.habilidades,
            perfil.idiomas,
            perfil.hoja_vida_url,
            perfil.linkedin_url,
            perfil.portafolio_url,
            perfil.disponibilidad,
            id_perfil
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_perfil: int):
        # Eliminación lógica: la fila NO se borra, solo cambia el estado.

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE perfiles_profesionales
            SET estado = FALSE,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_perfil = %s
            RETURNING id_perfil
        """, (id_perfil,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None
