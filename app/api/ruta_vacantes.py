from fastapi import APIRouter, HTTPException

from app.models.vacantes import Vacantes
from app.repositories.vacantes_repo import VacantesRepository


router = APIRouter(
    prefix="/vacantes",
    tags=["Gestión de vacantes"]
)

repo = VacantesRepository()


@router.get("/")
def listar_vacantes():
    return repo.obtener_todos()


@router.get("/{id_vacante}")
def obtener_vacante(id_vacante: int):

    vacante = repo.obtener_por_id(id_vacante)

    if not vacante:
        raise HTTPException(
            status_code=404,
            detail="Vacante no encontrada"
        )

    return vacante


@router.post("/")
def crear_vacante(vacante: Vacantes):

    nuevo_id = repo.crear(vacante)

    return {
        "mensaje": "Vacante registrada exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_vacante}")
def actualizar_vacante(
    id_vacante: int,
    vacante: Vacantes
):

    exito = repo.actualizar(
        id_vacante,
        vacante
    )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Vacante no encontrada"
        )

    return {
        "mensaje": "Vacante actualizada correctamente"
    }


@router.delete("/{id_vacante}")
def eliminar_vacante(id_vacante: int):

    exito = repo.eliminar(id_vacante)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Vacante no encontrada"
        )

    return {
        "mensaje": "Vacante eliminada correctamente"
    }