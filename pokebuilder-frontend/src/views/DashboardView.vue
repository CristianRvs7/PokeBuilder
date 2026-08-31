<script setup>
import { useRouter } from 'vue-router'
import ScanRing from '../components/ScanRing.vue'
import AppButton from '../components/AppButton.vue'
import { useAuth } from '../stores/auth.js'

const router = useRouter()
const auth = useAuth()

function handleLogout() {
  auth.clearSession()
  router.push('/login')
}
</script>

<template>
  <div class="dashboard">
    <div class="dashboard__card">
      <ScanRing state="success" :size="64" />
      <p class="dashboard__eyebrow">SESIÓN ACTIVA</p>
      <h1 class="dashboard__title">Bienvenido, {{ auth.state.user?.username || 'entrenador' }}</h1>
      <p class="dashboard__body">
        Tu cuenta quedó lista. El armador de equipos vive aquí próximamente: elige Pokémon,
        ajusta EVs/IVs y guarda tus builds para cada formato.
      </p>
      <AppButton variant="ghost" type="button" @click="handleLogout">Cerrar sesión</AppButton>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.dashboard__card {
  max-width: 420px;
  width: 100%;
  background: var(--color-panel-raised);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 40px 36px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

.dashboard__eyebrow {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-mint);
  margin: 4px 0 0;
}

.dashboard__title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 23px;
  margin: 0;
}

.dashboard__body {
  color: var(--color-text-muted);
  font-size: 14.5px;
  line-height: 1.6;
  margin: 0 0 6px;
}
</style>
