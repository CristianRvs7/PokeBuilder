<script setup>
import { reactive } from 'vue'
import ModalBase from './ModalBase.vue'
import AppInput from './AppInput.vue'
import AppButton from './AppButton.vue'

const props = defineProps({
  mode: { type: String, default: 'create' }, // create | edit
  team: { type: Object, default: null },
  saving: { type: Boolean, default: false },
  error: { type: String, default: '' },
})
const emit = defineEmits(['submit', 'close'])

const form = reactive({
  team_name: props.team?.team_name || '',
  description: props.team?.description || '',
  format: props.team?.format || '',
})
const errors = reactive({ team_name: '', description: '', format: '' })

function validate() {
  const name = form.team_name.trim()
  const description = form.description.trim()
  const format = form.format.trim()

  errors.team_name = name.length >= 1 && name.length <= 50 ? '' : 'Usa entre 1 y 50 caracteres.'
  errors.description =
    description.length >= 1 && description.length <= 250 ? '' : 'Cuéntanos algo breve (máx. 250 caracteres).'
  errors.format = format.length >= 1 && format.length <= 50 ? '' : 'Escribe un formato (máx. 50 caracteres).'

  return !errors.team_name && !errors.description && !errors.format
}

function handleSubmit() {
  if (!validate()) return
  emit('submit', {
    team_name: form.team_name.trim(),
    description: form.description.trim(),
    format: form.format.trim(),
  })
}
</script>

<template>
  <ModalBase @close="$emit('close')">
    <p class="modal-eyebrow">{{ mode === 'create' ? 'Nuevo equipo' : 'Editar equipo' }}</p>
    <h2 class="modal-title">{{ mode === 'create' ? 'Arma un equipo nuevo' : 'Ajusta los datos del equipo' }}</h2>

    <form class="auth-form" novalidate @submit.prevent="handleSubmit">
      <p v-if="error" class="form-banner" role="alert">{{ error }}</p>

      <AppInput v-model="form.team_name" label="Nombre del equipo" :error="errors.team_name" />
      <AppInput
        v-model="form.format"
        label="Formato"
        hint="Ej. VGC Reg H, OU, Doubles"
        :error="errors.format"
      />
      <AppInput
        v-model="form.description"
        label="Descripción"
        multiline
        :rows="3"
        hint="Una idea breve de la estrategia del equipo."
        :error="errors.description"
      />

      <div class="modal-actions">
        <AppButton type="button" variant="ghost" @click="$emit('close')">Cancelar</AppButton>
        <AppButton :loading="saving">{{ mode === 'create' ? 'Crear equipo' : 'Guardar cambios' }}</AppButton>
      </div>
    </form>
  </ModalBase>
</template>
