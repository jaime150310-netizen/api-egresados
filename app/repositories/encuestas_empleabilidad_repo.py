from app.core.database import Database
from app.models.encuestas_empleabilidad import EncuestasEmpleabilidad


class EncuestasEmpleabilidadRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM encuestas_empleabilidad
            ORDER BY id_encuesta ASC
        """)

        encuestas = cursor.fetchall()

        cursor.close()
        conn.close()

        return encuestas

    def obtener_por_id(self, id_encuesta: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM encuestas_empleabilidad
            WHERE id_encuesta = %s
        """, (id_encuesta,))

        encuesta = cursor.fetchone()

        cursor.close()
        conn.close()

        return encuesta

    def crear(self, encuesta: EncuestasEmpleabilidad):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO encuestas_empleabilidad
            (
                id_egresado,
                fecha_respuesta,
                esta_empleado,
                empresa_actual,
                cargo_actual,
                area_laboral,
                tipo_contrato,
                modalidad_trabajo,
                salario,
                relacion_carrera,
                tiempo_conseguir_empleo,
                esta_buscando_empleo,
                satisfaccion_laboral,
                observaciones
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING id_encuesta
        """, (
            encuesta.id_egresado,
            encuesta.fecha_respuesta,
            encuesta.esta_empleado,
            encuesta.empresa_actual,
            encuesta.cargo_actual,
            encuesta.area_laboral,
            encuesta.tipo_contrato,
            encuesta.modalidad_trabajo,
            encuesta.salario,
            encuesta.relacion_carrera,
            encuesta.tiempo_conseguir_empleo,
            encuesta.esta_buscando_empleo,
            encuesta.satisfaccion_laboral,
            encuesta.observaciones
        ))

        nuevo_id = cursor.fetchone()["id_encuesta"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(
        self,
        id_encuesta: int,
        encuesta: EncuestasEmpleabilidad
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE encuestas_empleabilidad
            SET id_egresado = %s,
                fecha_respuesta = %s,
                esta_empleado = %s,
                empresa_actual = %s,
                cargo_actual = %s,
                area_laboral = %s,
                tipo_contrato = %s,
                modalidad_trabajo = %s,
                salario = %s,
                relacion_carrera = %s,
                tiempo_conseguir_empleo = %s,
                esta_buscando_empleo = %s,
                satisfaccion_laboral = %s,
                observaciones = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_encuesta = %s
            RETURNING id_encuesta
        """, (
            encuesta.id_egresado,
            encuesta.fecha_respuesta,
            encuesta.esta_empleado,
            encuesta.empresa_actual,
            encuesta.cargo_actual,
            encuesta.area_laboral,
            encuesta.tipo_contrato,
            encuesta.modalidad_trabajo,
            encuesta.salario,
            encuesta.relacion_carrera,
            encuesta.tiempo_conseguir_empleo,
            encuesta.esta_buscando_empleo,
            encuesta.satisfaccion_laboral,
            encuesta.observaciones,
            id_encuesta
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_encuesta: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM encuestas_empleabilidad
            WHERE id_encuesta = %s
            RETURNING id_encuesta
        """, (id_encuesta,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None