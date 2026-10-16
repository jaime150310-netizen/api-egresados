from app.core.database import Database
from app.models.roles import Roles


class RolesRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM roles
            ORDER BY id_rol ASC
        """)

        roles = cursor.fetchall()

        cursor.close()
        conn.close()

        return roles

    def obtener_por_id(self, id_rol: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM roles
            WHERE id_rol = %s
        """, (id_rol,))

        rol = cursor.fetchone()

        cursor.close()
        conn.close()

        return rol

    def crear(self, rol: Roles):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO roles
            (nombre, descripcion)
            VALUES (%s, %s)
            RETURNING id_rol
        """, (
            rol.nombre,
            rol.descripcion
        ))

        nuevo_id = cursor.fetchone()["id_rol"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(self, id_rol: int, rol: Roles):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE roles
            SET nombre = %s,
                descripcion = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_rol = %s
            RETURNING id_rol
        """, (
            rol.nombre,
            rol.descripcion,
            id_rol
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_rol: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM roles
            WHERE id_rol = %s
            RETURNING id_rol
        """, (id_rol,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None