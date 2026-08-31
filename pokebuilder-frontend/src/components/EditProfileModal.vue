<script setup>
import { reactive } from 'vue'
import ModalBase from './ModalBase.vue'
import AppInput from './AppInput.vue'
import AppButton from './AppButton.vue'

const props = defineProps({
  user: { type: Object, default: null },
  saving: { type: Boolean, default: false },
  error: { type: String, default: '' },
})
const emit = defineEmits(['submit', 'close'])

const form = reactive({
  username: props.user?.username || '',
  email: props.user?.email || '',
  password: '',
})
const errors = reactive({ username: '', email: '', password: '' })

function validate() {
  const username = form.username.trim()
  const email = form.email.trim()

  errors.username = username.length >= 5 && username.length <= 20 ? '' : 'Usa entre 5 y 20 caracteres.'
  errors.email = /^\S+@\S+\.\S+$/.test(email) ? '' : 'Escribe un correo válido.'
  errors.password = !form.password || form.password.length >= 8 ? '' : 'Usa al menos 8 caracteres.'

  return !errors.username && !errors.email && !errors.password
}

function handleSubmit() {
  if (!validate()) return
  const payload = {
    username: form.username.trim(),
    email: form.email.trim(),
  }
  if (form.password) {
    payload.password = form.password
  }
  emit('submit', payload)
}
</script>

<template>
  <ModalBase @close="$emit('close')">
    <p class="modal-eyebrow">Tu cuenta</p>
    <h2 class="modal-title">Editar perfil</h2>

    <form class="auth-form" novalidate @submit.prevent="handleSubmit">
      <p v-if="error" class="form-banner" role="alert">{{ error }}</p>

      <AppInput v-model="form.username" label="Usuario" :error="errors.username" autocomplete="username" />
      <AppInput
        v-model="form.email"
        label="Correo"
        type="email"
        :error="errors.email"
        autocomplete="email"
      />
      <AppInput
        v-model="form.password"
        label="Nueva contraseña"
        type="password"
        hint="Déjalo en blanco para mantener tu contraseña actual."
        :error="errors.password"
        autocomplete="new-password"
      />

      <div class="modal-actions">
        <AppButton type="button" variant="ghost" @click="$emit('close')">Cancelar</AppButton>
        <AppButton :loading="saving">Guardar cambios</AppButton>
      </div>
    </form>
  </ModalBase>
</template>
