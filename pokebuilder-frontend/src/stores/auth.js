import { reactive, readonly } from 'vue'

const TOKEN_KEY = 'pb_token'
const USER_KEY = 'pb_user'

const state = reactive({
  token: localStorage.getItem(TOKEN_KEY) || null,
  user: safeParse(localStorage.getItem(USER_KEY)),
})

function safeParse(raw) {
  try {
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function setSession(token, user) {
  state.token = token
  state.user = user
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

function clearSession() {
  state.token = null
  state.user = null
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

// Actualiza el usuario en cache (por ejemplo tras editar el perfil) sin
// tocar el token de sesión.
function updateUser(user) {
  state.user = user
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function useAuth() {
  return {
    state: readonly(state),
    setSession,
    clearSession,
    updateUser,
    isAuthenticated: () => !!state.token,
  }
}
