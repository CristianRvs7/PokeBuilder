<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthLayout from '../components/AuthLayout.vue'
import AppInput from '../components/AppInput.vue'
import AppButton from '../components/AppButton.vue'
import { loginUser, fetchCurrentUser } from '../services/api.js'
import { useAuth } from '../stores/auth.js'

const router = useRouter()
const auth = useAuth()

const form = reactive({ identifier: '', password: '' })
const errors = reactive({ identifier: '', password: '' })
const formError = ref('')
const ringState = ref('idle')
const loading = ref(false)

function validate() {
  errors.identifier = form.identifier.trim() ? '' : 'Escribe tu usuario o correo.'
  errors.password = form.password ? '' : 'Escribe tu contraseña.'
  return !errors.identifier && !errors.password
}

async function handleSubmit() {
  formError.value = ''
  if (!validate()) return

  loading.value = true
  ringState.value = 'loading'
  try {
    const { access_token } = await loginUser({
      identifier: form.identifier.trim(),
      password: form.password,
    })
    const user = await fetchCurrentUser(access_token)
    auth.setSession(access_token, user)
    ringState.value = 'success'
    router.push('/')
  } catch (err) {
    ringState.value = 'error'
    formError.value = err.detail || 'Usuario o contraseña incorrectos.'
    loading.value = false
    setTimeout(() => {
      if (ringState.value === 'error') ringState.value = 'idle'
    }, 1800)
  }
}
</script>

<template>
  <AuthLayout
    eyebrow="ACCESO DE ENTRENADOR"
    title="Bienvenido de vuelta"
    subtitle="Inicia sesión para seguir armando tu equipo."
    :ring-state="ringState"
  >
    <form class="auth-form" novalidate @submit.prevent="handleSubmit">
      <p v-if="formError" class="form-banner" role="alert">{{ formError }}</p>

      <AppInput
        v-model="form.identifier"
        label="Usuario o correo"
        autocomplete="username"
        :error="errors.identifier"
      />
      <AppInput
        v-model="form.password"
        label="Contraseña"
        type="password"
        autocomplete="current-password"
        :error="errors.password"
      />

      <AppButton :loading="loading">Iniciar sesión</AppButton>

      <p class="auth-form__switch">
        ¿No tienes cuenta?
        <router-link to="/register">Crea una</router-link>
      </p>
    </form>
  </AuthLayout>
</template>
