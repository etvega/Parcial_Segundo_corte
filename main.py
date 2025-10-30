from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database.connection import Base, engine
from operations.cursos import router as cursos_router
from operations.estudiantes import router as estudiantes_router
from operations.matriculas import router as matriculas_router

# 🔹 Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# 🔹 Inicializar la aplicación FastAPI
app = FastAPI(
    title="Sistema Universidad ",
    description="API para gestionar cursos, estudiantes y matrículas",
    version="1.0.0",
    contact={
        "name": "Tatiana Vega",
        "email": "tatiana@example.com"
    },
)

# 🔹 Configuración de CORS (permite que cualquier frontend acceda)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia * por la URL del frontend si lo tienes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Incluir los routers de cada módulo
app.include_router(cursos_router)
app.include_router(estudiantes_router)
app.include_router(matriculas_router)

# 🔹 Ruta raíz para probar la API
@app.get("/")
def home():
    return {"mensaje": "Bienvenido al Sistema de Universidad "}

# 🔹 Ruta para evitar el error 404 del favicon
@app.get("/favicon.ico")
def favicon():
    # Puedes cambiar el return por un FileResponse si tienes un ícono real
    return {}

# 🔹 Evento opcional de inicio (solo informativo)
@app.on_event("startup")
def startup_event():
    print("El Servidor a iniciado correctamente y base de datos conectada.")
