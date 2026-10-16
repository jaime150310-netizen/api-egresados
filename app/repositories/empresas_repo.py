from app.core.database import Database
from app.models.empresas import Empresas


class EmpresasRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM empresas
            ORDER BY id_empresa ASC
        """)

        empresas = cursor.fetchall()

        cursor.close()
        conn.close()

        return empresas

    def obtener_por_id(self, id_empresa: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM empresas
            WHERE id_empresa = %s
        """, (id_empresa,))

        empresa = cursor.fetchone()

        cursor.close()
        conn.close()

        return empresa

    def crear(self, empresa: Empresas):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO empresas
            (
                nombre,
                identificacion_fiscal,
                direccion,
                ciudad,
                telefono,
                correo,
                persona_contacto,
                sector_economico,
                descripcion,
                estado
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            RETURNING id_empresa
        """, (
            empresa.nombre,
            empresa.identificacion_fiscal,
            empresa.direccion,
            empresa.ciudad,
            empresa.telefono,
            empresa.correo,
            empresa.persona_contacto,
            empresa.sector_economico,
            empresa.descripcion,
            empresa.estado
        ))

        nuevo_id = cursor.fetchone()["id_empresa"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(self, id_empresa: int, empresa: Empresas):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE empresas
            SET nombre = %s,
                identificacion_fiscal = %s,
                direccion = %s,
                ciudad = %s,
                telefono = %s,
                correo = %s,
                persona_contacto = %s,
                sector_economico = %s,
                descripcion = %s,
                estado = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_empresa = %s
            RETURNING id_empresa
        """, (
            empresa.nombre,
            empresa.identificacion_fiscal,
            empresa.direccion,
            empresa.ciudad,
            empresa.telefono,
            empresa.correo,
            empresa.persona_contacto,
            empresa.sector_economico,
            empresa.descripcion,
            empresa.estado,
            id_empresa
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_empresa: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM empresas
            WHERE id_empresa = %s
            RETURNING id_empresa
        """, (id_empresa,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None