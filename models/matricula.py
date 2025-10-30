from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"))
    curso_id = Column(Integer, ForeignKey("cursos.id"))
    fecha_matricula = Column(DateTime, default=datetime.utcnow)
    archivada = Column(Boolean, default=False)  # 👈 Nuevo campo

    estudiante = relationship("Estudiante", back_populates="matriculas")
    curso = relationship("Curso", back_populates="matriculas")
