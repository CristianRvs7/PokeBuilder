<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { createTeam, deleteTeam, fetchTeams, updateTeam } from '../services/api.js'
import { useAuth } from '../stores/auth.js'
import ScanRing from '../components/ScanRing.vue'
import AppButton from '../components/AppButton.vue'
import TeamCard from '../components/TeamCard.vue'
import TeamFormModal from '../components/TeamFormModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const router = useRouter()
const { state, clearSession } = useAuth()

const teams = ref([])
const loading = ref(true)
const loadError = ref('')

const modal = reactive({ open: false, mode: 'create', team: null, saving: false, error: '' })
const confirmState = reactive({ open: false, team: null, busy: false, error: '' })

async function loadTeams() {
  loading.value = true
  loadError.value = ''
  try {
    teams.value = await fetchTeams(state.token)
  } catch (err) {
    loadError.value = err.detail || 'No pudimos cargar tus equipos.'
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  modal.mode = 'create'
  modal.team = null
  modal.error = ''
  modal.open = true
}

function openEditModal(team) {
  modal.mode = 'edit'
  modal.team = team
  modal.error = ''
  modal.open = true
}

function closeModal() {
  modal.open = false
}

async function handleModalSubmit(payload) {
  modal.saving = true
  modal.error = ''
  try {
    if (modal.mode === 'create') {
      const created = await createTeam(state.token, payload)
      teams.value = [created, ...teams.value]
    } else {
      const updated = await updateTeam(state.token, modal.team.id, payload)
      teams.value = teams.value.map((team) => (team.id === updated.id ? updated : team))
    }
    modal.open = false
  } catch (err) {
    modal.error = err.detail || 'No pudimos guardar el equipo.'
  } finally {
    modal.saving = false
  }
}

function openDeleteConfirm(team) {
  confirmState.team = team
  confirmState.error = ''
  confirmState.open = true
}

function closeConfirm() {
  confirmState.open = false
}

async function handleConfirmDelete() {
  confirmState.busy = true
  confirmState.error = ''
  try {
    await deleteTeam(state.token, confirmState.team.id)
    teams.value = teams.value.filter((team) => team.id !== confirmState.team.id)
    confirmState.open = false
  } catch (err) {
    confirmState.error = err.detail || 'No pudimos eliminar el equipo.'
  } finally {
    confirmState.busy = false
  }
}

function goToTeam(id) {
  router.push(`/teams/${id}`)
}

function handleLogout() {
  clearSession()
  router.push('/login')
}

onMounted(loadTeams)
</script>

<template>
  <div class="teams-page">
    <header class="teams-page__header">
      <div class="teams-page__brand">
        <ScanRing state="idle" :size="42" />
        <div>
          <p class="teams-page__eyebrow">Diario de PokéBuilder</p>
          <h1 class="teams-page__title">Hola, {{ state.user?.username || 'entrenador' }}</h1>
        </div>
      </div>
      <AppButton type="button" variant="ghost" @click="handleLogout">Cerrar sesión</AppButton>
    </header>

    <main class="teams-page__main">
      <div class="teams-page__toolbar">
        <div>
          <h2 class="teams-page__section-title">Tus equipos</h2>
          <p class="teams-page__section-subtitle">Arma, ajusta y organiza tus builds competitivos.</p>
        </div>
        <AppButton type="button" class="teams-page__create" @click="openCreateModal">+ Crear equipo</AppButton>
      </div>

      <p v-if="loadError" class="form-banner" role="alert">{{ loadError }}</p>

      <div v-if="loading" class="teams-page__state">Cargando tus equipos…</div>

      <div v-else-if="teams.length === 0" class="teams-empty">
        <p class="teams-empty__title">Todavía no tienes equipos</p>
        <p class="teams-empty__body">Crea el primero para empezar a planear tu estrategia.</p>
        <AppButton type="button" @click="openCreateModal">Crear mi primer equipo</AppButton>
      </div>

      <div v-else class="teams-grid">
        <TeamCard
          v-for="team in teams"
          :key="team.id"
          :team="team"
          @open="goToTeam(team.id)"
          @edit="openEditModal(team)"
          @delete="openDeleteConfirm(team)"
        />
      </div>
    </main>

    <TeamFormModal
      v-if="modal.open"
      :mode="modal.mode"
      :team="modal.team"
      :saving="modal.saving"
      :error="modal.error"
      @submit="handleModalSubmit"
      @close="closeModal"
    />

    <ConfirmDialog
      v-if="confirmState.open"
      title="¿Eliminar este equipo?"
      :message="`Vas a eliminar «${confirmState.team?.team_name}». Esta acción no se puede deshacer.`"
      :busy="confirmState.busy"
      :error="confirmState.error"
      @confirm="handleConfirmDelete"
      @cancel="closeConfirm"
    />
  </div>
</template>

<style scoped>
.teams-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.teams-page__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 40px;
}

.teams-page__brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.teams-page__eyebrow {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-mint);
  margin: 0;
}

.teams-page__title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 21px;
  margin: 2px 0 0;
}

.teams-page__main {
  flex: 1;
  width: 100%;
  max-width: 1080px;
  margin: 0 auto;
  padding: 12px 40px 64px;
}

.teams-page__toolbar {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.teams-page__section-title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 24px;
  margin: 0 0 4px;
}

.teams-page__section-subtitle {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 14px;
}

.teams-page__create {
  width: auto;
}

.teams-page__state {
  color: var(--color-text-muted);
  font-size: 14.5px;
  padding: 40px 0;
  text-align: center;
}

.teams-empty {
  background: var(--color-panel-raised);
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-lg);
  padding: 48px 32px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.teams-empty__title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 19px;
  margin: 0;
}

.teams-empty__body {
  color: var(--color-text-muted);
  margin: 0 0 14px;
  font-size: 14px;
}

.teams-empty .btn {
  width: auto;
}

.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

@media (max-width: 640px) {
  .teams-page__header,
  .teams-page__main {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>
