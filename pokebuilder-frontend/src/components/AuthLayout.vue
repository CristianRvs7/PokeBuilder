<script setup>
import ScanRing from './ScanRing.vue'

defineProps({
  eyebrow: { type: String, default: '' },
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  ringState: { type: String, default: 'idle' },
})
</script>

<template>
  <div class="auth-shell">
    <aside class="journal">
      <div class="journal__badge">
        <ScanRing :state="ringState" :size="76" />
      </div>
      <p class="journal__eyebrow">Diario de PokéBuilder</p>
      <h1 class="journal__title">Arma, guarda y ajusta tus equipos competitivos</h1>

      <ol class="journal__route">
        <li class="journal__stop">
          <span class="journal__marker"></span>
          <div>
            <p class="journal__stop-title">Explora</p>
            <p class="journal__stop-body">Busca y conoce a cada Pokémon.</p>
          </div>
        </li>
        <li class="journal__stop">
          <span class="journal__marker"></span>
          <div>
            <p class="journal__stop-title">Arma tu equipo</p>
            <p class="journal__stop-body">Combina hasta 6 Pokémon por formato.</p>
          </div>
        </li>
        <li class="journal__stop">
          <span class="journal__marker"></span>
          <div>
            <p class="journal__stop-title">Ajusta la estrategia</p>
            <p class="journal__stop-body">EVs, IVs y movimientos, a tu manera.</p>
          </div>
        </li>
        <li class="journal__stop">
          <span class="journal__marker"></span>
          <div>
            <p class="journal__stop-title">Compite</p>
            <p class="journal__stop-body">Lleva tu equipo a la batalla.</p>
          </div>
        </li>
      </ol>

      <ul class="journal__notes">
        <li>Hasta 6 Pokémon por equipo</li>
        <li>Tus equipos quedan guardados, listos cuando vuelvas</li>
        <li>Próximamente: EVs, IVs y movimientos</li>
      </ul>
    </aside>

    <main class="panel">
      <div class="card">
        <p class="card__eyebrow">{{ eyebrow }}</p>
        <h2 class="card__title">{{ title }}</h2>
        <p v-if="subtitle" class="card__subtitle">{{ subtitle }}</p>
        <slot />
      </div>
    </main>
  </div>
</template>

<style scoped>
.auth-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(260px, 30%) 1fr;
}

.journal {
  position: relative;
  background: radial-gradient(circle at 18% 20%, rgba(63, 125, 88, 0.16), transparent 55%), var(--color-panel);
  border-right: 1px solid var(--color-border);
  padding: 48px 40px;
  display: flex;
  flex-direction: column;
  gap: 22px;
  overflow: hidden;
}

.journal::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: radial-gradient(var(--color-border) 1.4px, transparent 1.4px);
  background-size: 22px 22px;
  opacity: 0.6;
  pointer-events: none;
}

.journal__badge,
.journal__eyebrow,
.journal__title,
.journal__notes {
  position: relative;
}

.journal__eyebrow {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 12.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-mint);
  margin: 0;
}

.journal__title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: clamp(24px, 2.6vw, 32px);
  line-height: 1.25;
  margin: 0;
  max-width: 20ch;
}

.journal__notes {
  margin: auto 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
  font-size: 14px;
  color: var(--color-text-muted);
}

.journal__route {
  position: relative;
  margin: 4px 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.journal__route::before {
  content: '';
  position: absolute;
  left: 4px;
  top: 4px;
  bottom: 4px;
  border-left: 2px dashed var(--color-border);
}

.journal__stop {
  position: relative;
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.journal__marker {
  flex: none;
  width: 9px;
  height: 9px;
  margin-top: 5px;
  border-radius: 50%;
  background: var(--color-mint);
  box-shadow: 0 0 0 4px var(--color-panel);
  position: relative;
  z-index: 1;
}

.journal__stop-title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 15px;
  margin: 0 0 2px;
}

.journal__stop-body {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
  line-height: 1.4;
}

.journal__notes li {
  position: relative;
  padding-left: 22px;
  line-height: 1.4;
}

.journal__notes li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 6px;
  width: 8px;
  height: 8px;
  background: var(--color-gold);
  border-radius: 2px;
  transform: rotate(45deg);
}

.panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
}

.card {
  width: 100%;
  max-width: 380px;
  background: var(--color-panel-raised);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 36px 32px;
  box-shadow: 0 18px 40px -24px rgba(43, 33, 24, 0.35);
}

.card__eyebrow {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-coral);
  margin: 0 0 10px;
}

.card__title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 25px;
  margin: 0 0 6px;
}

.card__subtitle {
  color: var(--color-text-muted);
  margin: 0 0 26px;
  font-size: 14.5px;
  line-height: 1.5;
}

@media (max-width: 860px) {
  .auth-shell {
    grid-template-columns: 1fr;
  }
  .journal {
    padding: 32px 24px;
    border-right: none;
    border-bottom: 1px solid var(--color-border);
  }
  .journal__route {
    display: none;
  }
  .journal__notes {
    display: none;
  }
  .journal__title {
    max-width: none;
  }
}
</style>
