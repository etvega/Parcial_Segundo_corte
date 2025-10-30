🎓 Sistema Universidad

Proyecto desarrollado con FastAPI para la gestión académica de una universidad.
Permite administrar estudiantes, cursos y matrículas mediante endpoints RESTful documentados.

🧩 Características principales

CRUD completo para estudiantes, cursos y matrículas

Relación muchos a muchos entre estudiantes y cursos

Filtros en las consultas (semestre, créditos, códigos)

Manejo de errores (200, 201, 400, 404, 409)

Validaciones Pydantic

Documentación automática con Swagger UI

Conexión a base de datos SQLite

Proyecto modular y organizado

🗂️ Estructura del proyecto
Sistema_universidad/
│
├── main.py
├── database/
│   └── connection.py
├── models/
│   ├── estudiante.py
│   ├── curso.py
│   └── matricula.py
├── operations/
│   ├── estudiantes.py
│   ├── cursos.py
│   └── matriculas.py
├── schemas/
│   ├── estudiante_schema.py
│   ├── curso_schema.py
│   └── matricula_schema.py
├── requirements.txt
├── .gitignore
├── README.md
└── universidad.db

⚙️ Instalación y ejecución

Clonar el repositorio

git clone https://github.com/etvega/Sistema_universidad.git
cd Sistema_universidad


Crear entorno virtual (opcional pero recomendado)

python -m venv venv
source venv/Scripts/activate  # En Windows


Instalar dependencias

pip install -r requirements.txt


Ejecutar el servidor

uvicorn main:app --reload


Abrir la documentación interactiva

Swagger UI → 👉 http://127.0.0.1:8000/docs

ReDoc → 👉 http://127.0.0.1:8000/redoc

🧠 Endpoints principales
🧍‍♂️ Estudiantes
Método	Endpoint	Descripción
POST	/estudiantes/	Crear estudiante
GET	/estudiantes/	Listar estudiantes (filtro: semestre)
GET	/estudiantes/{id}	Obtener estudiante por ID
PUT	/estudiantes/{id}	Actualizar estudiante
DELETE	/estudiantes/{id}	Eliminar estudiante
GET	/estudiantes/{id}/cursos	Ver cursos matriculados
📘 Cursos
Método	Endpoint	Descripción
POST	/cursos/	Crear curso
GET	/cursos/	Listar cursos (filtros: créditos, códigos)
GET	/cursos/{id}	Obtener curso por ID
PUT	/cursos/{id}	Actualizar curso
DELETE	/cursos/{id}	Eliminar curso
GET	/cursos/{id}/estudiantes	Ver estudiantes matriculados
📝 Matrículas
Método	Endpoint	Descripción
POST	/matriculas/	Matricular estudiante en curso
GET	/matriculas/	Listar matrículas
GET	/matriculas/{id}	Obtener matrícula
DELETE	/matriculas/{id}	Desmatricular estudiante
🧩 Reglas de negocio

Un estudiante no puede matricularse dos veces en el mismo curso.

No se pueden crear, actualizar o eliminar entidades inexistentes.

Las matrículas eliminadas se marcan como archivadas (no se borran físicamente).

⚠️ Manejo de errores
Código	Significado	Caso de uso
200	OK	Petición exitosa
201	Created	Recurso creado
400	Bad Request	Datos inválidos
404	Not Found	No encontrado
409	Conflict	Duplicado o conflicto (ej. estudiante ya matriculado)
👩‍💻 Autora

Erika Tatiana Vega Joya
Proyecto académico – Sistema de Gestión Universitaria con FastAPI