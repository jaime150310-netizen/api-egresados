from fastapi import APIRouter, HTTPException

from app.models.perfiles_profesionales import PerfilesProfesionales
from app.repositories.perfiles_profesionales_repo import (
    PerfilesProfesionalesRepository
)


router = APIRouter(
    prefix="/perfiles_profesionales",
    tags=["Gestión de perfiles profesionales"]
)

repo = PerfilesProfesionalesRepository()


@router.get("/")
def listar_perfiles():
    return repo.obtener_todos()


@router.get("/{id_perfil}")
def obtener_perfil(id_perfil: int):

    perfil = repo.obtener_por_id(id_perfil)

    if not perfil:
        raise HTTPException(
            status_code=404,
            detail="Perfil profesional no encontrado"
        )

    return perfil


@router.post("/")
def crear_perfil(perfil: PerfilesProfesionales):

    nuevo_id = repo.crear(perfil)

    return {
        "mensaje": "Perfil profesional registrado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_perfil}")
def actualizar_perfil(
    id_perfil: int,
    perfil: PerfilesProfesionales
):

    exito = repo.actualizar(
        id_perfil,
        perfil
    )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Perfil profesional no encontrado"
        )

    return {
        "mensaje": "Perfil profesional actualizado correctamente"
    }


@router.delete("/{id_perfil}")
def eliminar_perfil(id_perfil: int):

    exito = repo.eliminar(id_perfil)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Perfil profesional no encontrado"
        )

    return {
        "mensaje": "Perfil profesional eliminado correctamente"
    }