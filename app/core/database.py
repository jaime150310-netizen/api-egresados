import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# En tu computador lee el archivo .env. En Render lee las variables de entorno del servicio.
load_dotenv()


class ErrorConexion(Exception):
    """Se lanza cuando la API no logra conectarse a la base de datos (Neon)."""


class Database:

    def __init__(self):
        # Forma sencilla: una sola variable DATABASE_URL (la "connection string" que da Neon).
        self.url = os.getenv("DATABASE_URL")

        # Forma alternativa: variables separadas.
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = os.getenv("DB_PORT") or "5432"

    def get_connection(self):
        try:
            if self.url:
                return psycopg2.connect(
                    self.url,
                    cursor_factory=RealDictCursor,
                    connect_timeout=15
                )

            return psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                sslmode=os.getenv("DB_SSLMODE", "require"),
                connect_timeout=15,
                cursor_factory=RealDictCursor
            )

        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            raise ErrorConexion(str(e))
