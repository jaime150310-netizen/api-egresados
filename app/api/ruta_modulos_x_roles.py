from fastapi import APIRouter, HTTPException

from app.models.modulos_x_roles import ModulosXRoles
from app.repositories.modulos_x_roles_repo import ModulosXRolesRepository


router = APIRouter(
    prefix="/modulos_x_roles",
    tags=["Gestión de permisos"]
)

repo = ModulosXRolesRepository()


@router.get("/")
def listar_permisos():
    return repo.obtener_todos()


@router.get("/{id_modulo_rol}")
def obtener_permiso(id_modulo_rol: int):

    permiso = repo.obtener_por_id(id_modulo_rol)

    if not permiso:
        raise HTTPException(
            status_code=404,
            detail="Permiso no encontrado"
        )

    return permiso


@router.post("/")
def crear_permiso(permiso: ModulosXRoles):

    nuevo_id = repo.crear(permiso)

    return {
        "mensaje": "Permiso registrado exitosamente",
        "id": nuevo_id
    }


@router.put("/{id_modulo_rol}")
def actualizar_permiso(
    id_modulo_rol: int,
    permiso: ModulosXRoles
):

    exito = repo.actualizar(
        id_modulo_rol,
        permiso
    )

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Permiso no encontrado"
        )

    return {
        "mensaje": "Permiso actualizado correctamente"
    }


@router.delete("/{id_modulo_rol}")
def eliminar_permiso(id_modulo_rol: int):

    exito = repo.eliminar(id_modulo_rol)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Permiso no encontrado"
        )

    return {
        "mensaje": "Permiso eliminado correctamente"
    }