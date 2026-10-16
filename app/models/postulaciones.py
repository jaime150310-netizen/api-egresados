from pydantic import BaseModel
from typing import Optional


class Postulaciones(BaseModel):

    id_postulacion: Optional[int] = None

    id_egresado: int
    id_vacante: int

    estado: str = "Pendiente"
    comentarios: Optional[str] = None