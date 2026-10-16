from pydantic import BaseModel
from typing import Optional


class ModulosXRoles(BaseModel):

    id_modulo_rol: Optional[int] = None

    id_rol: int
    id_modulo: int

    puede_ver: bool = False
    puede_crear: bool = False
    puede_actualizar: bool = False
    puede_eliminar: bool = False