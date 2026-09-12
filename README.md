# PokeBuilder

PokeBuilder es una aplicación web para crear, organizar y administrar equipos de Pokémon. Cada usuario puede registrarse, iniciar sesión y mantener múltiples equipos, agregando Pokémon en distintos *slots* y conservando la información de forma persistente.

El proyecto utiliza una API REST desarrollada con FastAPI, PostgreSQL y SQLAlchemy, protegida mediante autenticación JWT con OAuth2. La interfaz está construida con Vue y Vite, y los datos de Pokémon se consultan desde [PokeAPI](https://pokeapi.co/).

## Demo en vivo

- **Aplicación:** https://pokebuilder-frontend.onrender.com
- **API / Documentación interactiva (Swagger):** https://pokebuilder-2dvs.onrender.com/docs

> El backend corre en el plan gratuito de Render. Si nadie lo ha usado en los últimos 15 minutos, la primera petición puede tardar 30-60 segundos en responder mientras el servicio "despierta". Las siguientes son instantáneas.

## Funcionalidades

- Registro e inicio de sesión de usuarios.
- Autenticación y autorización mediante JWT y OAuth2.
- Creación de múltiples equipos por usuario.
- Consulta de información de Pokémon desde PokeAPI.
- Incorporación de Pokémon en los *slots* de cada equipo.
- Edición y eliminación de miembros.
- Edición y eliminación de equipos.
- Persistencia de usuarios y equipos en PostgreSQL.
- Interfaz web separada del backend.

## Tecnologías

### Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT y OAuth2
- Uvicorn

### Frontend

- Vue
- Vite
- JavaScript
- npm

### Despliegue

- Render (backend y frontend)
- Neon (PostgreSQL serverless)

### Servicio externo

- [PokeAPI](https://pokeapi.co/)

## Estructura aproximada del proyecto

```text
PokeBuilder/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── pokebuilder-frontend/
│   ├── .env.example
│   ├── .gitignore
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   └── src/
│       ├── assets/
│       │   └── main.css
│       ├── components/
│       │   ├── AppButton.vue
│       │   ├── AppInput.vue
│       │   ├── AuthLayout.vue
│       │   ├── ConfirmDialog.vue
│       │   ├── MemberFormModal.vue
│       │   ├── ModalBase.vue
│       │   ├── RosterSlot.vue
│       │   ├── ScanRing.vue
│       │   ├── TeamCard.vue
│       │   ├── TeamFormModal.vue
│       │   └── TrailBadge.vue
│       ├── router/
│       │   └── index.js
│       ├── services/
│       │   └── api.js
│       ├── stores/
│       │   └── auth.js
│       ├── views/
│       │   ├── DashboardView.vue
│       │   ├── LoginView.vue
│       │   ├── RegisterView.vue
│       │   ├── TeamDetailView.vue
│       │   └── TeamsView.vue
│       ├── App.vue
│       └── main.js
└── src/
    ├── main.py
    ├── core/
    ├── database/
    │   ├── create_tables.py
    │   ├── db_config.py
    │   └── schema.sql
    ├── models/
    │   └── db_schema.py
    ├── routes/
    │   ├── auth_routes.py
    │   ├── members_router.py
    │   └── team_routes.py
    ├── schemas/
    │   ├── members_schemas.py
    │   ├── team_schemas.py
    │   └── user_schemas.py
    └── services/
        ├── pokeapi.py
        ├── team_service.py
        └── user_service.py
```

## Requisitos

- Python 3.10 o superior.
- PostgreSQL.
- Node.js 18 o superior.
- npm.
- Git.

## Instalación del backend

1. Clona el repositorio y entra en su carpeta:

   ```bash
   git clone https://github.com/CristianRvs7/PokeBuilder
   cd PokeBuilder
   ```

2. Crea un entorno virtual:

   ```bash
   python -m venv .venv
   ```

3. Activa el entorno virtual.

   En Windows:

   ```powershell
   .venv\Scripts\activate
   ```

   En macOS o Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

5. Crea la base de datos PostgreSQL que utilizará la aplicación.


## Ejecución del backend

Desde la raíz de `PokeBuilder`, con el entorno virtual activado, ejecuta:

```bash
uvicorn src.main:app --reload
```

La API estará disponible normalmente en:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Instalación y ejecución del frontend

1. Entra en la carpeta del frontend:

   ```bash
   cd pokebuilder-frontend
   ```

2. Instala las dependencias:

   ```bash
   npm install
   ```

3. Inicia el servidor de desarrollo:

   ```bash
   npm run dev
   ```

Vite mostrará la dirección local de la aplicación, habitualmente `http://localhost:5173`.

## Endpoints principales

Las rutas exactas pueden variar según la implementación. A alto nivel, la API incluye endpoints para:

| Área | Operaciones principales |
| --- | --- |
| Autenticación | Registrar usuarios, iniciar sesión y generar tokens de acceso |
| Usuarios | Consultar la información del usuario autenticado |
| Equipos | Crear, listar, consultar, editar y eliminar equipos |
| Miembros | Agregar Pokémon, editar un *slot* y eliminar miembros |
| Pokémon | Consultar o procesar información obtenida desde PokeAPI |

La especificación actualizada puede consultarse en `/docs` mientras el backend está en ejecución.

## Estado del proyecto

PokeBuilder está desplegado y en funcionamiento (backend y frontend en Render, base de datos en Neon). El proyecto sigue en desarrollo activo: la autenticación y la gestión de equipos ya están operativas, pero la estructura, los endpoints y la interfaz pueden seguir cambiando conforme avance.

## Futuras mejoras

- Validar reglas de composición y límites de los equipos.
- Incorporar búsqueda avanzada y filtros de Pokémon.
- Mostrar tipos, habilidades, estadísticas y movimientos.
- Añadir análisis de fortalezas y debilidades del equipo.
- Mejorar la experiencia de usuario y el diseño adaptable.
- Implementar pruebas automatizadas para backend y frontend.
- Añadir migraciones de base de datos.
- Preparar el despliegue y la integración continua.

## Autor

Desarrollado por **Cristian Umaña**.

- LinkedIn: [Cristian Umaña](https://www.linkedin.com/in/cristian-umaña/)