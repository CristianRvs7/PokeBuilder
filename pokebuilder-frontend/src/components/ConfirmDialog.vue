<script setup>
import ModalBase from './ModalBase.vue'
import AppButton from './AppButton.vue'

defineProps({
  title: { type: String, default: '¿Estás seguro?' },
  message: { type: String, default: '' },
  confirmLabel: { type: String, default: 'Eliminar' },
  cancelLabel: { type: String, default: 'Cancelar' },
  busy: { type: Boolean, default: false },
  error: { type: String, default: '' },
})
defineEmits(['confirm', 'cancel'])
</script>

<template>
  <ModalBase @close="$emit('cancel')">
    <p class="modal-eyebrow">Confirmar</p>
    <h2 class="modal-title">{{ title }}</h2>
    <p v-if="message" class="confirm-message">{{ message }}</p>
    <p v-if="error" class="form-banner" role="alert">{{ error }}</p>

    <div class="modal-actions">
      <AppButton type="button" variant="ghost" @click="$emit('cancel')">{{ cancelLabel }}</AppButton>
      <AppButton type="button" :loading="busy" @click="$emit('confirm')">{{ confirmLabel }}</AppButton>
    </div>
  </ModalBase>
</template>
