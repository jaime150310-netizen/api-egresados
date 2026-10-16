from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.repositories.auth_repo import AuthRepository


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

repo = AuthRepository()


class LoginDatos(BaseModel):
    correo: str
    contrasena: str
    id_rol: int


@router.post("/login")
def login(datos: LoginDatos):

    usuario = repo.buscar_usuario(datos.correo)

    if not usuario or usuario["contrasena"] != datos.contrasena:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    if usuario["id_rol"] != datos.id_rol:
        raise HTTPException(
            status_code=403,
            detail="Tu cuenta no pertenece al rol seleccionado"
        )

    return {
        "id_usuario": usuario["id_usuario"],
        "nombre": f'{usuario["nombre"]} {usuario["apellido"]}',
        "correo": usuario["correo"],
        "id_rol": usuario["id_rol"],
        "rol": usuario["rol"],
        "modulos": repo.modulos_del_rol(usuario["id_rol"])
    }


@router.get("/modulos/{id_rol}")
def modulos_de_un_rol(id_rol: int):
    return repo.modulos_del_rol(id_rol)
