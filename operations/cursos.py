from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from models.curso import Curso
from models.matricula import Matricula
from schemas.curso_schema import CursoSchema, CursoCreate, CursoUpdate

router = APIRouter(tags=["Cursos"])


@router.post("/cursos/", response_model=CursoSchema, status_code=status.HTTP_201_CREATED)
def crear_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    """
    📘 Crea un curso nuevo.
    - **Valida:** que el código no esté duplicado.
    - **Retorna:** curso creado.
    """
    existe = db.query(Curso).filter(Curso.codigo == curso.codigo).first()
    if existe:
        raise HTTPException(status_code=409, detail="El código ya está registrado")

    nuevo = Curso(**curso.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/cursos/", response_model=List[CursoSchema], status_code=status.HTTP_200_OK)
def listar_cursos(creditos: int | None = None, codigo: str | None = None, db: Session = Depends(get_db)):
    """
    📗 Lista todos los cursos o filtra por número de créditos o código.
    - **Parámetros opcionales:** creditos, codigo.
    """
    query = db.query(Curso)
    if creditos:
        query = query.filter(Curso.creditos == creditos)
    if codigo:
        query = query.filter(Curso.codigo == codigo)
    return query.all()


@router.get("/cursos/{id}", status_code=status.HTTP_200_OK)
def obtener_curso_y_estudiantes(id: int, db: Session = Depends(get_db)):
    """
    📙 Muestra la información de un curso y sus estudiantes activos.
    - **Incluye:** estudiantes con matrícula no archivada.
    - **Error 404:** si el curso no existe.
    """
    curso = db.query(Curso).filter(Curso.id == id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    estudiantes = [
        {"id": m.estudiante.id, "nombre": m.estudiante.nombre, "cedula": m.estudiante.cedula}
        for m in curso.matriculas if not m.archivada
    ]
    return {"curso": curso, "estudiantes": estudiantes}


@router.put("/cursos/{id}", response_model=CursoSchema, status_code=status.HTTP_200_OK)
def actualizar_curso(id: int, datos: CursoUpdate, db: Session = Depends(get_db)):
    """
    ✏️ Actualiza un curso existente.
    - **Valida:** que se envíen datos (400) y que exista (404).
    """
    curso = db.query(Curso).filter(Curso.id == id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    cambios = datos.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    for key, value in cambios.items():
        setattr(curso, key, value)

    db.commit()
    db.refresh(curso)
    return curso


@router.delete("/cursos/{id}", status_code=status.HTTP_200_OK)
def eliminar_curso(id: int, db: Session = Depends(get_db)):
    """
    ❌ Elimina un curso y archiva las matrículas asociadas.
    - **Error 404:** si el curso no existe.
    """
    curso = db.query(Curso).filter(Curso.id == id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    matriculas = db.query(Matricula).filter(Matricula.curso_id == id).all()
    for m in matriculas:
        m.archivada = True

    db.delete(curso)
    db.commit()
    return {"mensaje": "Curso eliminado y matrículas archivadas"}
