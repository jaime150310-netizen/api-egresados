# Prueba rápida de conexión a Neon:   python test_db.py
from app.core.database import Database, ErrorConexion

try:
    conn = Database().get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT current_database() AS bd")
    print("====================================")
    print("CONEXIÓN EXITOSA con la base de datos:", cursor.fetchone()["bd"])
    print("====================================")
    cursor.close()
    conn.close()
except ErrorConexion as e:
    print("NO SE PUDO CONECTAR:", e)
