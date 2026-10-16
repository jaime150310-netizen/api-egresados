from pydantic import BaseModel
from typing import Optional


class Empresas(BaseModel):

    id_empresa: Optional[int] = None

    nombre: str
    identificacion_fiscal: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    persona_contacto: Optional[str] = None
    sector_economico: Optional[str] = None
    descripcion: Optional[str] = None

    estado: bool = True