from pydantic import BaseModel
from typing import Optional


class Egresados(BaseModel):

    id_egresado: Optional[int] = None

    id_usuario: int

    codigo_estudiante: Optional[str] = None
    programa_academico: str
    facultad: Optional[str] = None
    fecha_graduacion: str
    nivel_formacion: Optional[str] = None
    anio_graduacion: int

    estado: bool = True