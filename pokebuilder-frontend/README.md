# PokeBuilder — Frontend

Frontend en Vue 3 + Vite para el login y registro de PokeBuilder. Se conecta directo
a tu API de FastAPI existente.

## Poner en marcha

```bash
npm install
cp .env.example .env   # ajusta VITE_API_URL si tu backend no corre en localhost:8000
npm run dev
```

Se abre en `http://localhost:5173`.

## Importante: habilita CORS en el backend

Por defecto, FastAPI rechaza peticiones desde un origen distinto (Vite corre en el
puerto 5173, tu API en el 8000). Aplica el cambio que te dejo en `main.py` (adjunto
aparte) antes de probar el login/registro desde el navegador — si no, verás errores
de CORS en la consola aunque el backend esté funcionando bien.

## Qué incluye

- `LoginView` → `POST /login` (form-urlencoded, como espera tu `OAuth2PasswordRequestForm`)
  seguido de `GET /test-auth` para traer los datos del usuario.
- `RegisterView` → `POST /register` (JSON), con las mismas validaciones que tu
  `UserCreate` (usuario 5–20 caracteres, contraseña mínimo 8).
- `DashboardView` → placeholder simple post-login (ahí vivirá el armador de equipos).
- Guard de rutas en `router/index.js`: si no hay token no puedes entrar a `/`, y si ya
  iniciaste sesión no puedes ver `/login` ni `/register`.
- El token se guarda en `localStorage` (`pb_token` / `pb_user`).

## Estructura

```
src/
  components/   AuthLayout, AppInput, AppButton, ScanRing (elemento de firma visual)
  views/        LoginView, RegisterView, DashboardView
  services/     api.js — un solo lugar que habla con el backend
  stores/       auth.js — sesión reactiva + localStorage
  router/       guard de autenticación
```
