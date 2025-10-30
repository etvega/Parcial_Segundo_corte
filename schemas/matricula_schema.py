# schemas/matricula_schema.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class MatriculaSchema(BaseModel):
    id: Optional[int] = None
    estudiante_id: int = Field(..., gt=0, description="ID del estudiante (mayor a 0)")
    curso_id: int = Field(..., gt=0, description="ID del curso (mayor a 0)")
    fecha_matricula: Optional[date] = Field(default_factory=date.today, description="Fecha de la matrícula")
    archivada: Optional[bool] = Field(default=False, description="Indica si la matrícula está archivada")

    class Config:
        from_attributes = True  # Compatible con Pydantic v2
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class MatriculaSchema(BaseModel):
    id: Optional[int] = None
    estudiante_id: int = Field(..., gt=0, description="ID del estudiante (mayor a 0)")
    curso_id: int = Field(..., gt=0, description="ID del curso (mayor a 0)")
    fecha_matricula: Optional[date] = Field(default_factory=date.today)
    archivada: Optional[bool] = Field(default=False, description="Indica si la matrícula está archivada")

    class Config:
        from_attributes = True
