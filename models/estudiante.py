from sqlalchemy import Column, Integer, String
from database.connection import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    semestre = Column(Integer, nullable=False)  # Nuevo campo
