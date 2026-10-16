from fastapi import APIRouter, HTTPException

from app.models.usuarios import Usuarios
from app.repositories.usuarios_repo import UsuariosRepository


router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de usuarios"]
)

repo = UsuariosRepository()


@router.get("/")
def listar_usuarios():
    return repo.obtener_todos()


@router.get("/{id_usuario}")
def obtener_usuario(id_usuario: int):

    usuario = repo.obtener_por_id(id_usuario)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.post("/")
def crear_usuario(usuario: Usuarios):

    nuevo_id = repo.crear(usuario)

    return {
        "mensaje": "Usuario registrado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_usuario}")
def actualizar_usuario(
    id_usuario: int,
    usuario: Usuarios
):

    exito = repo.actualizar(
        id_usuario,
        usuario
    )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "mensaje": "Usuario actualizado correctamente"
    }


@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: int):

    exito = repo.eliminar(id_usuario)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "mensaje": "Usuario eliminado correctamente"
    }