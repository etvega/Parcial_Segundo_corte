from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.estudiante import Estudiante
from models.matricula import Matricula
from schemas.estudiante_schema import EstudianteSchema, EstudianteCreate, EstudianteUpdate
from typing import List

router = APIRouter(tags=["Estudiantes"])

# ✅ Crear estudiante
@router.post("/estudiantes/", response_model=EstudianteSchema)
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
@router.get("/estudiantes/", response_model=List[EstudianteSchema])
def listar_estudiantes(semestre: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Estudiante)
    if semestre:
        query = query.filter(Estudiante.semestre == semestre)
    return query.all()


# ✅ Obtener estudiante con cursos matriculados
@router.get("/estudiantes/{id}")
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
@router.put("/estudiantes/{id}", response_model=EstudianteSchema)
def actualizar_estudiante(id: int, datos: EstudianteUpdate, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(estudiante, key, value)

    db.commit()
    db.refresh(estudiante)
    return estudiante


# ✅ Eliminar estudiante (archiva sus matrículas)
@router.delete("/estudiantes/{id}")
def eliminar_estudiante(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    matriculas = db.query(Matricula).filter(Matricula.estudiante_id == id).all()
    for m in matriculas:
        m.archivada = True

    db.delete(estudiante)
    db.commit()
    return {"mensaje": "Estudiante eliminado y matrículas archivadas"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.estudiante import Estudiante
from models.matricula import Matricula
from schemas.estudiante_schema import EstudianteSchema
from typing import List

router = APIRouter()

# ✅ Crear estudiante
@router.post("/estudiantes/", response_model=EstudianteSchema)
def crear_estudiante(estudiante: EstudianteSchema, db: Session = Depends(get_db)):
    existente = db.query(Estudiante).filter(Estudiante.cedula == estudiante.cedula).first()
    if existente:
        raise HTTPException(status_code=400, detail="La cédula ya está registrada")
    nuevo = Estudiante(**estudiante.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ✅ Listar estudiantes (filtro: semestre)
@router.get("/estudiantes/", response_model=List[EstudianteSchema])
def listar_estudiantes(semestre: int = None, db: Session = Depends(get_db)):
    query = db.query(Estudiante)
    if semestre:
        query = query.filter(Estudiante.semestre == semestre)
    return query.all()


# ✅ Obtener estudiante con cursos matriculados
@router.get("/estudiantes/{id}")
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


# ✅ Actualizar estudiante
@router.put("/estudiantes/{id}", response_model=EstudianteSchema)
def actualizar_estudiante(id: int, datos: EstudianteSchema, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    for key, value in datos.dict().items():
        setattr(estudiante, key, value)

    db.commit()
    db.refresh(estudiante)
    return estudiante


# ✅ Eliminar estudiante (archiva sus matrículas)
@router.delete("/estudiantes/{id}")
def eliminar_estudiante(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    matriculas = db.query(Matricula).filter(Matricula.estudiante_id == id).all()
    for m in matriculas:
        m.archivada = True

    db.delete(estudiante)
    db.commit()
    return {"mensaje": "Estudiante eliminado y matrículas archivadas"}
