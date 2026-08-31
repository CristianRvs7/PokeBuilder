const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// El backend devuelve mensajes en inglés (detail). Los traducimos para
// mantener el frontend en español y darle voz consistente a la interfaz.
const ERROR_TRANSLATIONS = {
  'Username already in use': 'Ese nombre de usuario ya está en uso. Prueba con otro.',
  'Email already in use': 'Ese correo ya tiene una cuenta asociada.',
  'Invalid Credentials': 'Usuario o contraseña incorrectos.',
  'Invalid Token': 'Tu sesión expiró. Inicia sesión de nuevo.',
  'Error creating user': 'No pudimos crear la cuenta. Intenta de nuevo en un momento.',
  'Team not found': 'No encontramos ese equipo.',
  'Pokemon not found': 'No encontramos ese Pokémon. Revisa el nombre o el número.',
  'Member not found': 'Ese Pokémon ya no está en el equipo.',
  'Error, please check the information': 'Revisa los datos e intenta de nuevo.',
  'Username already exists': 'Ese nombre de usuario ya está en uso. Prueba con otro.',
  'Email already exists': 'Ese correo ya tiene una cuenta asociada.',
}

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.detail = message
    this.status = status
  }
}

function translateDetail(raw) {
  if (Array.isArray(raw)) {
    // Errores de validación de Pydantic: [{ loc, msg, type }, ...]
    return raw.map((item) => item.msg).join(' ')
  }
  if (typeof raw === 'string') {
    return ERROR_TRANSLATIONS[raw] || raw
  }
  return 'Ha ocurrido un error inesperado. Intenta de nuevo.'
}

async function parseError(response) {
  try {
    const data = await response.json()
    return translateDetail(data?.detail)
  } catch {
    return 'Ha ocurrido un error inesperado. Intenta de nuevo.'
  }
}

async function request(path, options) {
  let response
  try {
    response = await fetch(`${BASE_URL}${path}`, options)
  } catch {
    throw new ApiError('No pudimos conectar con el servidor. ¿Está corriendo el backend?', 0)
  }
  if (!response.ok) {
    const detail = await parseError(response)
    throw new ApiError(detail, response.status)
  }
  if (response.status === 204) {
    return null
  }
  return response.json()
}

export function registerUser({ username, email, password }) {
  return request('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  })
}

export function loginUser({ identifier, password }) {
  // /login usa OAuth2PasswordRequestForm: el campo "username" acepta
  // tanto el username real como el correo (ver get_user_by_identifier).
  const body = new URLSearchParams()
  body.set('username', identifier)
  body.set('password', password)

  return request('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  })
}

export function fetchCurrentUser(token) {
  return request('/test-auth', {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function updateCurrentUser(token, payload) {
  return request('/users/me', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })
}

// --- Equipos ---
// Nota: /teams/ lleva la barra final porque así está registrada la ruta
// en el backend (prefix '/teams' + path '/'); sin ella, FastAPI redirige.

export function fetchTeams(token) {
  return request('/teams/', {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function fetchTeamById(token, teamId) {
  return request(`/teams/${teamId}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function createTeam(token, { team_name, description, format }) {
  return request('/teams/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ team_name, description, format }),
  })
}

export function updateTeam(token, teamId, payload) {
  return request(`/teams/edit/${teamId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })
}

export function deleteTeam(token, teamId) {
  return request(`/teams/${teamId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
}

// --- Miembros del equipo (Pokémon) ---
// Nota: a diferencia de /teams/*, estas rutas viven en la raíz porque así
// están registradas en members_router.py (APIRouter sin prefix). El PATCH
// además usa "member" en singular, no "members" como el resto. Si algún día
// se homologa el backend, solo hay que tocar los paths de acá abajo.

export function searchPokemon(nameOrId) {
  return request(`/pokemon/${encodeURIComponent(nameOrId.trim().toLowerCase())}`)
}

export function fetchTeamMembers(token, teamId) {
  return request(`/${teamId}/members`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export function addTeamMember(token, teamId, payload) {
  return request(`/${teamId}/members`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })
}

export function updateTeamMember(token, teamId, slot, payload) {
  return request(`/${teamId}/member/${slot}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })
}

export function deleteTeamMember(token, teamId, slot) {
  return request(`/${teamId}/members/${slot}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
}
