from fastapi import APIRouter, HTTPException

from app.models.egresados import Egresados
from app.repositories.egresados_repo import EgresadosRepository


router = APIRouter(
    prefix="/egresados",
    tags=["Gestión de egresados"]
)

repo = EgresadosRepository()


@router.get("/")
def listar_egresados():
    return repo.obtener_todos()


@router.get("/{id_egresado}")
def obtener_egresado(id_egresado: int):

    egresado = repo.obtener_por_id(id_egresado)

    if not egresado:
        raise HTTPException(
            status_code=404,
            detail="Egresado no encontrado"
        )

    return egresado


@router.post("/")
def crear_egresado(egresado: Egresados):

    nuevo_id = repo.crear(egresado)

    return {
        "mensaje": "Egresado registrado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_egresado}")
def actualizar_egresado(
    id_egresado: int,
    egresado: Egresados
):

    exito = repo.actualizar(
        id_egresado,
        egresado
    )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Egresado no encontrado"
        )

    return {
        "mensaje": "Egresado actualizado correctamente"
    }


@router.delete("/{id_egresado}")
def eliminar_egresado(id_egresado: int):

    exito = repo.eliminar(id_egresado)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Egresado no encontrado"
        )

    return {
        "mensaje": "Egresado eliminado correctamente"
    }