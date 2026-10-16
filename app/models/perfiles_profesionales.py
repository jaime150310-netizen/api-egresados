from pydantic import BaseModel
from typing import Optional


class PerfilesProfesionales(BaseModel):

    id_perfil: Optional[int] = None

    id_egresado: int

    perfil_profesional: Optional[str] = None
    cargo_deseado: Optional[str] = None
    area_interes: Optional[str] = None
    experiencia_anios: Optional[float] = None
    habilidades: Optional[str] = None
    idiomas: Optional[str] = None
    hoja_vida_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portafolio_url: Optional[str] = None
    disponibilidad: Optional[str] = None