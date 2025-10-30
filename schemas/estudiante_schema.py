# schemas/estudiante_schema.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class EstudianteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre del estudiante")
    apellido: str = Field(..., min_length=2, max_length=50, description="Apellido del estudiante")
    correo: EmailStr = Field(..., description="Correo electrónico válido del estudiante")
    cedula: str = Field(..., min_length=6, max_length=12, description="Cédula única del estudiante")
    semestre: int = Field(..., ge=1, le=12, description="Semestre actual (1 a 12)")

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    apellido: Optional[str] = Field(None, min_length=2, max_length=50)
    correo: Optional[EmailStr] = None
    semestre: Optional[int] = Field(None, ge=1, le=12)

class EstudianteSchema(EstudianteBase):
    id: int

    class Config:
        from_attributes = True
