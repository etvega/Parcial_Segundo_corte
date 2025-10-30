# Sistema Universidad - Proyecto FastAPI

Proyecto desarrollado con **FastAPI** que permite la gestión de estudiantes, cursos y matrículas en una universidad.

---



## Estructura del proyecto

```
Sistema_universidad/
│
├── main.py
│
├── database/
│   └── connection.py
│
├── models/
│   ├── estudiante.py
│   ├── curso.py
│   └── matricula.py
│
├── operations/
│   ├── estudiantes.py
│   ├── cursos.py
│   └── matriculas.py
│
├── schemas/
│   ├── estudiante_schema.py
│   ├── curso_schema.py
│   └── matricula_schema.py
│
├── requirements.txt
├── .gitignore
├── README.md
└── universidad.db
```

---

## Instalación y configuración

1. **Clonar el repositorio**

```bash
git clone https://github.com/tuusuario/Sistema_universidad.git
cd Sistema_universidad
```

2. **Crear y activar un entorno virtual**

```bash
python -m venv venv
venv\Scripts\activate
```

*(En Mac/Linux usa `source venv/bin/activate`)*

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Ejecutar el proyecto**

```bash
uvicorn main:app --reload
```

---

## Endpoints principales

### 👩‍🎓 Estudiantes

| Método | Ruta | Descripción |
|--------|------|--------------|
| `POST` | `/estudiantes/` | Crear estudiante |
| `GET` | `/estudiantes/` | Listar estudiantes |
| `GET` | `/estudiantes/?semestre=` | Filtrar por semestre |
| `GET` | `/estudiantes/{id}` | Obtener estudiante y cursos matriculados |
| `PUT` | `/estudiantes/{id}` | Actualizar estudiante |
| `DELETE` | `/estudiantes/{id}` | Eliminar estudiante |

### 📚 Cursos

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/cursos/` | Crear curso |
| `GET` | `/cursos/` | Listar cursos |
| `GET` | `/cursos/?creditos=` | Filtrar por créditos |
| `GET` | `/cursos/{id}` | Obtener curso y estudiantes matriculados |
| `PUT` | `/cursos/{id}` | Actualizar curso |
| `DELETE` | `/cursos/{id}` | Eliminar curso |

### 📝 Matrículas

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/matriculas/` | Matricular estudiante en curso |
| `GET` | `/matriculas/` | Listar matrículas |
| `GET` | `/matriculas/{id}` | Obtener matrícula |
| `DELETE` | `/matriculas/{id}` | Desmatricular estudiante (archivar) |

---

## ⚠️ Manejo de errores HTTP

| Código | Descripción |
|--------|--------------|
| `200` | Respuesta exitosa |
| `201` | Recurso creado correctamente |
| `400` | Error en la solicitud (datos inválidos) |
| `404` | Recurso no encontrado |
| `409` | Conflicto (por ejemplo, matrícula duplicada) |

---

## 🧠 Lógica de negocio implementada

- Un estudiante **no puede matricularse dos veces** en el mismo curso.  
- No se pueden crear registros **sin validar campos obligatorios**.  
- Las matrículas eliminadas se **archivan**, no se borran físicamente.  
- Se pueden obtener estudiantes con sus cursos y viceversa.

---

## 🧩 Dependencias principales

- fastapi  
- uvicorn  
- sqlalchemy  
- pydantic  
- sqlite3

Instaladas automáticamente desde `requirements.txt`.

---

## 📖 Documentación interactiva

Una vez ejecutado el servidor, puedes acceder a la documentación generada automáticamente:

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 💬 Autor

**Erika Tatiana Vega Joya**  
Proyecto académico - Universidad Catolica de Colombia 
2025
