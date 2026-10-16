from app.core.database import Database
from app.models.usuarios import Usuarios


class UsuariosRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            ORDER BY id_usuario ASC
        """)

        usuarios = cursor.fetchall()

        cursor.close()
        conn.close()

        return usuarios

    def obtener_por_id(self, id_usuario: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE id_usuario = %s
        """, (id_usuario,))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        return usuario

    def crear(self, usuario: Usuarios):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios
            (
                id_rol,
                nombre,
                apellido,
                correo,
                contrasena,
                celular,
                direccion,
                ciudad,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_usuario
        """, (
            usuario.id_rol,
            usuario.nombre,
            usuario.apellido,
            usuario.correo,
            usuario.contrasena,
            usuario.celular,
            usuario.direccion,
            usuario.ciudad,
            usuario.estado
        ))

        nuevo_id = cursor.fetchone()["id_usuario"]

        conn.commit()

        cursor.close()
        conn.close()

        return nuevo_id

    def actualizar(self, id_usuario: int, usuario: Usuarios):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE usuarios
            SET id_rol = %s,
                nombre = %s,
                apellido = %s,
                correo = %s,
                contrasena = %s,
                celular = %s,
                direccion = %s,
                ciudad = %s,
                estado = %s,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id_usuario = %s
            RETURNING id_usuario
        """, (
            usuario.id_rol,
            usuario.nombre,
            usuario.apellido,
            usuario.correo,
            usuario.contrasena,
            usuario.celular,
            usuario.direccion,
            usuario.ciudad,
            usuario.estado,
            id_usuario
        ))

        actualizado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return actualizado is not None

    def eliminar(self, id_usuario: int):

        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Primero se borra lo que depende de este egresado
        cursor.execute("DELETE FROM postulaciones WHERE id_egresado IN (SELECT id_egresado FROM egresados WHERE id_usuario = %s)", (id_usuario,))
        cursor.execute("DELETE FROM encuestas_empleabilidad WHERE id_egresado IN (SELECT id_egresado FROM egresados WHERE id_usuario = %s)", (id_usuario,))
        cursor.execute("DELETE FROM perfiles_profesionales WHERE id_egresado IN (SELECT id_egresado FROM egresados WHERE id_usuario = %s)", (id_usuario,))
        cursor.execute("DELETE FROM egresados WHERE id_usuario = %s", (id_usuario,))


        cursor.execute("""
            DELETE FROM usuarios
            WHERE id_usuario = %s
            RETURNING id_usuario
        """, (id_usuario,))

        eliminado = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return eliminado is not None