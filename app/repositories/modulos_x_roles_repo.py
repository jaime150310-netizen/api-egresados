from app.core.database import Database
from app.models.modulos_x_roles import ModulosXRoles


class ModulosXRolesRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM modulos_x_roles
            ORDER BY id_modulo_rol ASC
        """)

        permisos = cursor.fetchall()

        cursor.close()
        conn.close()

        return permisos

    def obtener_por_id(self, id_modulo_rol: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM modulos_x_roles
            WHERE id_modulo_rol = %s
        """, (id_modulo_rol,))

        permiso = cursor.fetchone()

        cursor.close()
        conn.close()

        return permiso

    def crear(self, permiso: ModulosXRoles):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO modulos_x_roles
            (
                id_rol,
                id_modulo,
                puede_ver,
                puede_crear,
                puede_actualizar,
                puede_eliminar
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_modulo_rol
        """, (
            permiso.id_rol,
            permiso.id_modulo,
            permiso.puede_ver,
            permiso.puede_crear,
            permiso.puede_actualizar,
            permiso.puede_eliminar
        ))

        nuevo_id = cursor.fetchone()["id_modulo_rol"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(self, id_modulo_rol: int, permiso: ModulosXRoles):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE modulos_x_roles
            SET id_rol = %s,
                id_modulo = %s,
                puede_ver = %s,
                puede_crear = %s,
                puede_actualizar = %s,
                puede_eliminar = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_modulo_rol = %s
            RETURNING id_modulo_rol
        """, (
            permiso.id_rol,
            permiso.id_modulo,
            permiso.puede_ver,
            permiso.puede_crear,
            permiso.puede_actualizar,
            permiso.puede_eliminar,
            id_modulo_rol
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_modulo_rol: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM modulos_x_roles
            WHERE id_modulo_rol = %s
            RETURNING id_modulo_rol
        """, (id_modulo_rol,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None