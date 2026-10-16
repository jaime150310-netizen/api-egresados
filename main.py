import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2 import errors as pg

from app.core.database import Database, ErrorConexion

from app.api import ruta_auth
from app.api import ruta_roles
from app.api import ruta_modulos
from app.api import ruta_modulos_x_roles
from app.api import ruta_usuarios
from app.api import ruta_egresados
from app.api import ruta_perfiles_profesionales
from app.api import ruta_empresas
from app.api import ruta_vacantes
from app.api import ruta_postulaciones
from app.api import ruta_encuestas_empleabilidad


app = FastAPI(
    title="API de Empleabilidad y Red de Egresados",
    description=(
        "API REST para gestionar usuarios, egresados, perfiles profesionales, "
        "empresas, vacantes, postulaciones y seguimiento de empleabilidad."
    ),
    version="1.0.0"
)


# CORS: permite que el frontend llame a esta API desde otro puerto o dominio.
# En la nube, define la variable ALLOWED_ORIGINS con la URL del frontend (varias separadas por coma).
origenes = ["http://localhost:5173", "http://127.0.0.1:5173"]
origenes += [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes,
    allow_origin_regex=r"https://.*\.(vercel\.app|netlify\.app)",
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Mensajes de error claros (en vez de "Internal Server Error").
# El frontend muestra el texto "detail" tal cual.
# ---------------------------------------------------------------------------
@app.exception_handler(ErrorConexion)
async def error_conexion(request, exc):
    return JSONResponse(
        status_code=503,
        content={"detail": "La API no puede conectarse a la base de datos. Revisa DATABASE_URL (o DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)."}
    )


@app.exception_handler(pg.UniqueViolation)
async def error_repetido(request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": "Ya existe un registro con esos datos (por ejemplo, un correo, celular o NIT repetido)."}
    )


@app.exception_handler(pg.ForeignKeyViolation)
async def error_relacion(request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": "No se puede completar: ese dato está relacionado con otros registros (por ejemplo, una empresa que tiene vacantes) o apunta a algo que no existe."}
    )


@app.exception_handler(pg.NotNullViolation)
async def error_faltante(request, exc):
    columna = getattr(getattr(exc, "diag", None), "column_name", None) or "un campo"
    return JSONResponse(status_code=400, content={"detail": f"Falta un dato obligatorio: {columna}."})


@app.exception_handler(psycopg2.Error)
async def error_base_de_datos(request, exc):
    primera_linea = str(exc).strip().splitlines()[0] if str(exc).strip() else "error desconocido"
    return JSONResponse(status_code=400, content={"detail": f"Error en la base de datos: {primera_linea}"})


app.include_router(ruta_auth.router)
app.include_router(ruta_roles.router)
app.include_router(ruta_modulos.router)
app.include_router(ruta_modulos_x_roles.router)
app.include_router(ruta_usuarios.router)
app.include_router(ruta_egresados.router)
app.include_router(ruta_perfiles_profesionales.router)
app.include_router(ruta_empresas.router)
app.include_router(ruta_vacantes.router)
app.include_router(ruta_postulaciones.router)
app.include_router(ruta_encuestas_empleabilidad.router)


@app.get("/")
def estado_api():
    return {
        "mensaje": "La API de Empleabilidad y Red de Egresados se encuentra en línea y funcional"
    }


@app.get("/salud")
def salud():
    """Abre esta dirección para comprobar que la API Y la base de datos están conectadas."""
    conn = Database().get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT current_database() AS bd")
    nombre_bd = cursor.fetchone()["bd"]
    cursor.execute("SELECT COUNT(*) AS total FROM roles")
    roles = cursor.fetchone()["total"]
    cursor.close()
    conn.close()
    return {
        "api": "en línea",
        "base_de_datos": "conectada",
        "nombre_bd": nombre_bd,
        "roles_en_la_bd": roles
    }
