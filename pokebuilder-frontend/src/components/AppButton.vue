<script setup>
defineProps({
  loading: { type: Boolean, default: false },
  type: { type: String, default: 'submit' },
  variant: { type: String, default: 'primary' },
})
</script>

<template>
  <button
    :type="type"
    class="btn"
    :class="[`btn--${variant}`, { 'is-loading': loading }]"
    :disabled="loading"
  >
    <span v-if="loading" class="btn__spinner" aria-hidden="true"></span>
    <span class="btn__label"><slot /></span>
  </button>
</template>

<style scoped>
.btn {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 15px;
  letter-spacing: 0.02em;
  padding: 13px 22px;
  border-radius: var(--radius-pill);
  border: 1px solid transparent;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  transition: transform 0.15s ease, opacity 0.15s ease, background 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

.btn:active {
  transform: scale(0.98);
}

.btn--primary {
  background: var(--color-coral);
  color: var(--color-panel-raised);
}
.btn--primary:hover:not(:disabled) {
  background: #a83d31;
}

.btn--ghost {
  background: transparent;
  border-color: var(--color-border);
  color: var(--color-text);
}
.btn--ghost:hover:not(:disabled) {
  border-color: var(--color-mint);
  color: var(--color-mint);
}

.btn--white {
  background: #ffffff;
  color: var(--color-mint);
  box-shadow: 0 4px 14px -6px rgba(20, 30, 45, 0.4);
}
.btn--white:hover:not(:disabled) {
  background: #f2f2f2;
}

.btn:disabled {
  opacity: 0.75;
  cursor: progress;
}

.btn__spinner {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid rgba(0, 0, 0, 0.25);
  border-top-color: currentColor;
  animation: spin 0.7s linear infinite;
}

.btn--ghost .btn__spinner {
  border: 2px solid rgba(43, 33, 24, 0.15);
  border-top-color: currentColor;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.btn:focus-visible {
  outline: 2px solid var(--color-mint);
  outline-offset: 2px;
}
</style>
