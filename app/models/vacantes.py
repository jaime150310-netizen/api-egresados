from pydantic import BaseModel
from typing import Optional


class Vacantes(BaseModel):

    id_vacante: Optional[int] = None

    id_empresa: int

    titulo: str
    descripcion: Optional[str] = None
    requisitos: Optional[str] = None
    area: Optional[str] = None
    cargo: Optional[str] = None
    modalidad: Optional[str] = None
    tipo_contrato: Optional[str] = None
    salario: Optional[float] = None
    ciudad: Optional[str] = None
    fecha_publicacion: Optional[str] = None
    fecha_cierre: Optional[str] = None
    estado: str = "Disponible"
    cupos: int = 1