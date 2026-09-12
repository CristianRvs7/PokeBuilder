from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth_routes, team_routes, members_router, moves_routes

app = FastAPI(
    title='PokeBuilder! :)',
    version='1.0.0'
)

# Necesario para que el frontend (Vite, puerto 5173) pueda llamar a esta API
# desde el navegador. Agrega aqui otros origenes si despliegas en otro dominio.
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_routes.router)
app.include_router(team_routes.router)
app.include_router(members_router.router)
app.include_router(moves_routes.router)