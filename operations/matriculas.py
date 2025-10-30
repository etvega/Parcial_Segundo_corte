from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.matricula  import Matricula
from models.estudiante import Estudiante
from models.curso import Curso
from schemas.matricula_schema import MatriculaSchema
from typing import List

router = APIRouter()


# ✅ Crear matrícula
@router.post("/matriculas/", response_model=MatriculaSchema)
def crear_matricula(estudiante_id: int, curso_id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    curso = db.query(Curso).filter(Curso.id == curso_id).first()

    if not estudiante or not curso:
        raise HTTPException(status_code=404, detail="Estudiante o curso no encontrado")

    existente = db.query(Matricula).filter(
        Matricula.estudiante_id == estudiante_id,
        Matricula.curso_id == curso_id,
        Matricula.archivada == False
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="El estudiante ya está matriculado en este curso")

    nueva = Matricula(estudiante_id=estudiante_id, curso_id=curso_id)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# ✅ Listar matrículas (opcional: incluir archivadas)
@router.get("/matriculas/", response_model=List[MatriculaSchema])
def listar_matriculas(incluir_archivadas: bool = False, db: Session = Depends(get_db)):
    query = db.query(Matricula)
    if not incluir_archivadas:
        query = query.filter(Matricula.archivada == False)
    return query.all()


# ✅ Obtener matrícula por ID
@router.get("/matriculas/{id}", response_model=MatriculaSchema)
def obtener_matricula(id: int, db: Session = Depends(get_db)):
    matricula = db.query(Matricula).filter(Matricula.id == id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    return matricula


# ✅ Desmatricular (archiva la matrícula)
@router.delete("/matriculas/{id}")
def desmatricular(id: int, db: Session = Depends(get_db)):
    matricula = db.query(Matricula).filter(Matricula.id == id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")

    matricula.archivada = True
    db.commit()
    return {"mensaje": "Matrícula archivada correctamente"}
