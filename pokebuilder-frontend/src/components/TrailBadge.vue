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
  <div class="trail-badge" :class="`is-${state}`" :style="{ width: size + 'px', height: size + 'px' }">
    <svg viewBox="0 0 100 100" class="trail-badge__svg">
      <circle class="badge-ring" cx="50" cy="50" r="44" />
      <circle class="badge-face" cx="50" cy="50" r="36" />
      <g class="badge-compass">
        <path class="compass-arm compass-arm--ns" d="M50 20 L58 50 L50 80 L42 50 Z" />
        <path class="compass-arm compass-arm--ew" d="M20 50 L50 42 L80 50 L50 58 Z" />
        <circle class="compass-core" cx="50" cy="50" r="5" />
      </g>
    </svg>
  </div>
</template>

<style scoped>
.trail-badge {
  display: inline-block;
}
.trail-badge__svg {
  width: 100%;
  height: 100%;
}

.badge-ring {
  fill: none;
  stroke: var(--color-meadow);
  stroke-width: 4;
  stroke-dasharray: 5 6;
  stroke-linecap: round;
  transition: stroke 0.25s ease;
}

.badge-face {
  fill: var(--color-cream);
  stroke: var(--color-border);
  stroke-width: 1;
}

.badge-compass {
  transform-origin: 50px 50px;
  animation: sway 4.5s ease-in-out infinite;
}

.compass-arm {
  transition: fill 0.25s ease;
}
.compass-arm--ns {
  fill: var(--color-berry);
}
.compass-arm--ew {
  fill: var(--color-bark-muted);
}
.compass-core {
  fill: var(--color-sun-deep);
  transition: fill 0.25s ease;
}

.is-loading .badge-compass {
  animation: spin 1.1s linear infinite;
}
.is-loading .badge-ring {
  stroke: var(--color-sun-deep);
}

.is-success .badge-compass {
  animation: settle 0.6s ease-out forwards;
}
.is-success .badge-ring {
  stroke: var(--color-meadow-deep);
}
.is-success .compass-arm--ns,
.is-success .compass-arm--ew {
  fill: var(--color-meadow-deep);
}
.is-success .compass-core {
  fill: var(--color-sun);
}

.is-error {
  animation: shake 0.45s ease-in-out;
}
.is-error .badge-ring {
  stroke: var(--color-berry);
}
.is-error .compass-arm--ns,
.is-error .compass-arm--ew {
  fill: var(--color-berry);
}

@keyframes sway {
  0%,
  100% {
    transform: rotate(-8deg);
  }
  50% {
    transform: rotate(8deg);
  }
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
@keyframes settle {
  0% {
    transform: rotate(0deg) scale(1);
  }
  50% {
    transform: rotate(0deg) scale(1.25);
  }
  100% {
    transform: rotate(0deg) scale(1);
  }
}
@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-4px);
  }
  75% {
    transform: translateX(4px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .badge-compass,
  .is-error {
    animation: none !important;
  }
}
</style>
