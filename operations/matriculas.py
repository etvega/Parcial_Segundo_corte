from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from models.matricula import Matricula
from models.estudiante import Estudiante
from models.curso import Curso
from schemas.matricula_schema import MatriculaSchema
from typing import List

router = APIRouter(tags=["Matrículas"])


@router.post("/matriculas/", response_model=MatriculaSchema, status_code=status.HTTP_201_CREATED)
def crear_matricula(estudiante_id: int, curso_id: int, db: Session = Depends(get_db)):
    """
    📘 Crea una nueva matrícula para un estudiante en un curso.
    - **Valida:** existencia de estudiante y curso.
    - **Evita duplicados (409)** y retorna la matrícula creada.
    """
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
        raise HTTPException(status_code=409, detail="El estudiante ya está matriculado en este curso")

    nueva = Matricula(estudiante_id=estudiante_id, curso_id=curso_id)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.get("/matriculas/", response_model=List[MatriculaSchema], status_code=status.HTTP_200_OK)
def listar_matriculas(incluir_archivadas: bool = False, db: Session = Depends(get_db)):
    """
    📗 Lista todas las matrículas registradas.
    - **Parámetro opcional:** incluir_archivadas (bool).
    """
    query = db.query(Matricula)
    if not incluir_archivadas:
        query = query.filter(Matricula.archivada == False)
    return query.all()


@router.get("/matriculas/{id}", response_model=MatriculaSchema, status_code=status.HTTP_200_OK)
def obtener_matricula(id: int, db: Session = Depends(get_db)):
    """
    📙 Obtiene una matrícula por su ID.
    - **Error 404:** si no existe.
    """
    matricula = db.query(Matricula).filter(Matricula.id == id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    return matricula


@router.delete("/matriculas/{id}", status_code=status.HTTP_200_OK)
def desmatricular(id: int, db: Session = Depends(get_db)):
    """
    ❌ Archiva (desmatricula) un registro activo.
    - **Error 404:** si no existe.
    - **Error 400:** si ya está archivada.
    """
    matricula = db.query(Matricula).filter(Matricula.id == id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")

    if matricula.archivada:
        raise HTTPException(status_code=400, detail="La matrícula ya está archivada")

    matricula.archivada = True
    db.commit()
    return {"mensaje": "Matrícula archivada correctamente"}
