from pydantic import BaseModel
from typing import Optional


class EncuestasEmpleabilidad(BaseModel):

    id_encuesta: Optional[int] = None

    id_egresado: int

    fecha_respuesta: Optional[str] = None

    esta_empleado: bool

    empresa_actual: Optional[str] = None
    cargo_actual: Optional[str] = None
    area_laboral: Optional[str] = None
    tipo_contrato: Optional[str] = None
    modalidad_trabajo: Optional[str] = None

    salario: Optional[float] = None

    relacion_carrera: Optional[bool] = None

    tiempo_conseguir_empleo: Optional[int] = None

    esta_buscando_empleo: Optional[bool] = None

    satisfaccion_laboral: Optional[float] = None

    observaciones: Optional[str] = None