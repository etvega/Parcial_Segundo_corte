# schemas/curso_schema.py
from pydantic import BaseModel, Field
from typing import Optional

class CursoBase(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=10, description="Código único del curso (ej: MAT101)")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del curso")
    creditos: int = Field(..., ge=1, le=10, description="Número de créditos (1 a 10)")
    descripcion: Optional[str] = Field(None, max_length=200, description="Descripción opcional del curso")

class CursoCreate(CursoBase):
    pass

class CursoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50, description="Nuevo nombre del curso")
    creditos: Optional[int] = Field(None, ge=1, le=10, description="Número de créditos (1 a 10)")
    descripcion: Optional[str] = Field(None, max_length=200, description="Nueva descripción")

class CursoSchema(CursoBase):
    id: int

    class Config:
        from_attributes = True  # Compatible con Pydantic v2
