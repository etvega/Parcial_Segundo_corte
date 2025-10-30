# operations/estudiantes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from models.estudiante import Estudiante
from models.matricula import Matricula
from schemas.estudiante_schema import EstudianteSchema, EstudianteCreate, EstudianteUpdate
from typing import List

router = APIRouter(tags=["Estudiantes"])

# ✅ Crear estudiante
@router.post("/estudiantes/", response_model=EstudianteSchema, status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    existente = db.query(Estudiante).filter(Estudiante.correo == estudiante.correo).first()
    if existente:
        raise HTTPException(status_code=409, detail="El correo ya está registrado")

    nuevo = Estudiante(**estudiante.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ✅ Listar estudiantes (con filtro por semestre)
@router.get("/estudiantes/", response_model=List[EstudianteSchema], status_code=status.HTTP_200_OK)
def listar_estudiantes(semestre: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Estudiante)
    if semestre:
        query = query.filter(Estudiante.semestre == semestre)
    estudiantes = query.all()

    if not estudiantes:
        raise HTTPException(status_code=404, detail="No se encontraron estudiantes con ese filtro")

    return estudiantes


# ✅ Obtener estudiante con cursos matriculados
@router.get("/estudiantes/{id}", status_code=status.HTTP_200_OK)
def obtener_estudiante_con_cursos(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    matriculas = db.query(Matricula).filter(
        Matricula.estudiante_id == id,
        Matricula.archivada == False
    ).all()

    cursos = [m.curso for m in matriculas]
    return {"estudiante": estudiante, "cursos": cursos}


# ✅ Actualizar estudiante (solo los campos enviados)
@router.put("/estudiantes/{id}", response_model=EstudianteSchema, status_code=status.HTTP_200_OK)
def actualizar_estudiante(id: int, datos: EstudianteUpdate, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    if datos.correo:
        correo_existente = db.query(Estudiante).filter(
            Estudiante.correo == datos.correo,
            Estudiante.id != id
        ).first()
        if correo_existente:
            raise HTTPException(status_code=409, detail="El correo ya está registrado por otro estudiante")

    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(estudiante, key, value)

    db.commit()
    db.refresh(estudiante)
    return estudiante


# ✅ Eliminar estudiante (archiva sus matrículas)
@router.delete("/estudiantes/{id}", status_code=status.HTTP_200_OK)
def eliminar_estudiante(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    matriculas = db.query(Matricula).filter(Matricula.estudiante_id == id).all()
    for m in matriculas:
        m.archivada = True

    db.delete(estudiante)
    db.commit()
    return {"mensaje": "Estudiante eliminado y matrículas archivadas correctamente"}
