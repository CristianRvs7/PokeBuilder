<script setup>
defineProps({
  state: {
    type: String,
    default: 'idle', // idle | loading | success | error
  },
  size: {
    type: Number,
    default: 84,
  },
})
</script>

<template>
  <div class="badge" :class="`is-${state}`" :style="{ width: size + 'px', height: size + 'px' }">
    <svg viewBox="0 0 100 100" class="badge__svg">
      <circle class="badge__rim" cx="50" cy="50" r="44" />
      <g class="badge__ticks">
        <line v-for="n in 12" :key="n" x1="50" y1="8" x2="50" y2="14" :transform="`rotate(${n * 30} 50 50)`" />
      </g>
      <g class="badge__needle">
        <polygon class="needle__north" points="50,20 44,50 56,50" />
        <polygon class="needle__south" points="50,80 44,50 56,50" />
      </g>
      <circle class="badge__core" cx="50" cy="50" r="5" />
    </svg>
  </div>
</template>

<style scoped>
.badge {
  display: inline-block;
}

.badge__svg {
  width: 100%;
  height: 100%;
}

.badge__rim {
  fill: none;
  stroke: var(--color-border);
  stroke-width: 3;
}

.badge__ticks line {
  stroke: var(--color-text-muted);
  stroke-width: 2;
  stroke-linecap: round;
  opacity: 0.55;
}

.needle__north {
  fill: var(--color-coral);
}
.needle__south {
  fill: var(--color-text-muted);
  opacity: 0.6;
}

.badge__core {
  fill: var(--color-panel-raised);
  stroke: var(--color-text);
  stroke-width: 2;
}

.badge__needle {
  transform-origin: 50px 50px;
  animation: settle 4s ease-in-out infinite;
}

@keyframes settle {
  0%, 100% { transform: rotate(-6deg); }
  50% { transform: rotate(6deg); }
}

/* Cargando: la aguja gira buscando señal */
.is-loading .badge__needle {
  animation: spin 0.9s linear infinite;
}
.is-loading .needle__north {
  fill: var(--color-coral);
}
.is-loading .badge__rim {
  stroke: var(--color-coral);
}

/* Éxito: la aguja se fija hacia arriba y el aro brilla en dorado */
.is-success .badge__needle {
  animation: none;
  transform: rotate(0deg);
}
.is-success .needle__north {
  fill: var(--color-mint);
}
.is-success .badge__rim {
  stroke: var(--color-gold);
  stroke-width: 4;
}

/* Error: la aguja tiembla, como una brújula que perdió el norte */
.is-error .badge__needle {
  animation: shake 0.4s ease-in-out;
}
.is-error .needle__north {
  fill: var(--color-coral);
}
.is-error .badge__rim {
  stroke: var(--color-coral);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes shake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-18deg); }
  75% { transform: rotate(18deg); }
}

@media (prefers-reduced-motion: reduce) {
  .badge__needle {
    animation: none !important;
  }
}
</style>
