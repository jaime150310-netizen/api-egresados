from app.core.database import Database


class AuthRepository:

    def __init__(self):
        self.db = Database()

    def buscar_usuario(self, correo: str):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.id_usuario, u.nombre, u.apellido, u.correo,
                   u.contrasena, u.id_rol, r.nombre AS rol
            FROM usuarios u
            JOIN roles r ON r.id_rol = u.id_rol
            WHERE LOWER(u.correo) = LOWER(%s)
            AND u.estado = TRUE
        """, (correo,))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        return usuario

    def modulos_del_rol(self, id_rol: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.nombre, m.descripcion,
                   mr.puede_ver, mr.puede_crear,
                   mr.puede_actualizar, mr.puede_eliminar
            FROM modulos_x_roles mr
            JOIN modulos m ON m.id_modulo = mr.id_modulo
            WHERE mr.id_rol = %s
            AND mr.puede_ver = TRUE
            ORDER BY m.id_modulo ASC
        """, (id_rol,))

        modulos = cursor.fetchall()

        cursor.close()
        conn.close()

        return modulos
