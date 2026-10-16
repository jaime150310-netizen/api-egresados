from fastapi import APIRouter, HTTPException

from app.models.encuestas_empleabilidad import EncuestasEmpleabilidad
from app.repositories.encuestas_empleabilidad_repo import (
    EncuestasEmpleabilidadRepository
)


router = APIRouter(
    prefix="/encuestas_empleabilidad",
    tags=["Seguimiento de empleabilidad"]
)

repo = EncuestasEmpleabilidadRepository()


@router.get("/")
def listar_encuestas():
    return repo.obtener_todos()


@router.get("/{id_encuesta}")
def obtener_encuesta(id_encuesta: int):

    encuesta = repo.obtener_por_id(id_encuesta)

    if not encuesta:
        raise HTTPException(
            status_code=404,
            detail="Encuesta de empleabilidad no encontrada"
        )

    return encuesta


@router.post("/")
def crear_encuesta(encuesta: EncuestasEmpleabilidad):

    nuevo_id = repo.crear(encuesta)

    return {
        "mensaje": "Encuesta de empleabilidad registrada exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_encuesta}")
def actualizar_encuesta(
    id_encuesta: int,
    encuesta: EncuestasEmpleabilidad
):

    exito = repo.actualizar(
        id_encuesta,
        encuesta
    )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Encuesta de empleabilidad no encontrada"
        )

    return {
        "mensaje": "Encuesta de empleabilidad actualizada correctamente"
    }


@router.delete("/{id_encuesta}")
def eliminar_encuesta(id_encuesta: int):

    exito = repo.eliminar(id_encuesta)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Encuesta de empleabilidad no encontrada"
        )

    return {
        "mensaje": "Encuesta de empleabilidad eliminada correctamente"
    }