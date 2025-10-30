from database.connection import Base, engine
from models.estudiante import Estudiante
from models.curso import Curso
from models.matricula import Matricula

# Crear todas las tablas
print(" Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas exitosamente.")
