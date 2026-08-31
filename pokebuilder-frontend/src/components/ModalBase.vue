<script setup>
import { onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['close'])

function handleKeydown(event) {
  if (event.key === 'Escape') emit('close')
}

onMounted(() => document.addEventListener('keydown', handleKeydown))
onUnmounted(() => document.removeEventListener('keydown', handleKeydown))
</script>

<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card" role="dialog" aria-modal="true">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(43, 33, 24, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 50;
}

.modal-card {
  width: 100%;
  max-width: 420px;
  max-height: 90vh;
  overflow-y: auto;
  background: var(--color-panel-raised);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 28px 26px;
  box-shadow: 0 30px 60px -20px rgba(43, 33, 24, 0.45);
}
</style>
