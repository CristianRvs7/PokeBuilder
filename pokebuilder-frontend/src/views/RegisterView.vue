<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthLayout from '../components/AuthLayout.vue'
import AppInput from '../components/AppInput.vue'
import AppButton from '../components/AppButton.vue'
import { registerUser } from '../services/api.js'

const router = useRouter()

const form = reactive({ username: '', email: '', password: '' })
const errors = reactive({ username: '', email: '', password: '' })
const formError = ref('')
const formSuccess = ref('')
const ringState = ref('idle')
const loading = ref(false)

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validate() {
  const username = form.username.trim()
  errors.username =
    username.length >= 5 && username.length <= 20 ? '' : 'Usa entre 5 y 20 caracteres.'
  errors.email = EMAIL_PATTERN.test(form.email.trim()) ? '' : 'Escribe un correo válido.'
  errors.password = form.password.length >= 8 ? '' : 'Usa al menos 8 caracteres.'
  return !errors.username && !errors.email && !errors.password
}

async function handleSubmit() {
  formError.value = ''
  formSuccess.value = ''
  if (!validate()) return

  loading.value = true
  ringState.value = 'loading'
  try {
    await registerUser({
      username: form.username.trim(),
      email: form.email.trim(),
      password: form.password,
    })
    ringState.value = 'success'
    formSuccess.value = 'Cuenta creada. Te llevamos a iniciar sesión…'
    setTimeout(() => router.push('/login'), 1600)
  } catch (err) {
    ringState.value = 'error'
    formError.value = err.detail || 'No pudimos crear la cuenta.'
    loading.value = false
    setTimeout(() => {
      if (ringState.value === 'error') ringState.value = 'idle'
    }, 1800)
  }
}
</script>

<template>
  <AuthLayout
    eyebrow="REGISTRO DE ENTRENADOR"
    title="Crea tu perfil de entrenador"
    subtitle="Guarda tus equipos y ajústalos cuando quieras."
    :ring-state="ringState"
  >
    <form class="auth-form" novalidate @submit.prevent="handleSubmit">
      <p v-if="formError" class="form-banner" role="alert">{{ formError }}</p>
      <p v-if="formSuccess" class="form-banner form-banner--success" role="status">
        {{ formSuccess }}
      </p>

      <AppInput
        v-model="form.username"
        label="Usuario"
        autocomplete="username"
        hint="Entre 5 y 20 caracteres."
        :error="errors.username"
      />
      <AppInput
        v-model="form.email"
        label="Correo electrónico"
        type="email"
        autocomplete="email"
        :error="errors.email"
      />
      <AppInput
        v-model="form.password"
        label="Contraseña"
        type="password"
        autocomplete="new-password"
        hint="Mínimo 8 caracteres."
        :error="errors.password"
      />

      <AppButton :loading="loading">Crear cuenta</AppButton>

      <p class="auth-form__switch">
        ¿Ya tienes cuenta?
        <router-link to="/login">Inicia sesión</router-link>
      </p>
    </form>
  </AuthLayout>
</template>
