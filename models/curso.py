from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.connection import Base

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)  # ⚡ Código único
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    creditos = Column(Integer, nullable=False)

    # Relación con matrícula
    matriculas = relationship("Matricula", back_populates="curso")
