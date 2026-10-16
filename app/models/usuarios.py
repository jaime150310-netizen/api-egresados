from pydantic import BaseModel
from typing import Optional


class Usuarios(BaseModel):

    id_usuario: Optional[int] = None

    id_rol: int

    nombre: str
    apellido: str
    correo: str
    contrasena: str

    celular: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None

    estado: bool = True