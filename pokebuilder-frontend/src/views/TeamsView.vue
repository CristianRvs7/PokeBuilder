<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { createTeam, deleteTeam, fetchTeamMembers, fetchTeams, updateTeam } from '../services/api.js'
import { useAuth } from '../stores/auth.js'
import AppHeader from '../components/AppHeader.vue'
import AppButton from '../components/AppButton.vue'
import TeamListItem from '../components/TeamListItem.vue'
import TeamFormModal from '../components/TeamFormModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const router = useRouter()
const { state } = useAuth()

const teams = ref([])
const loading = ref(true)
const loadError = ref('')

// Roster de cada equipo, cargado aparte para no bloquear la lista mientras
// llegan los sprites (no hay endpoint que devuelva equipos + miembros juntos).
const membersByTeam = reactive({})

const modal = reactive({ open: false, mode: 'create', team: null, saving: false, error: '' })
const confirmState = reactive({ open: false, team: null, busy: false, error: '' })

async function loadTeams() {
  loading.value = true
  loadError.value = ''
  try {
    teams.value = await fetchTeams(state.token)
    loadMembersForTeams(teams.value)
  } catch (err) {
    loadError.value = err.detail || 'No pudimos cargar tus equipos.'
  } finally {
    loading.value = false
  }
}

function loadMembersForTeams(teamList) {
  teamList.forEach(async (team) => {
    try {
      membersByTeam[team.id] = await fetchTeamMembers(state.token, team.id)
    } catch {
      membersByTeam[team.id] = []
    }
  })
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
      membersByTeam[created.id] = []
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
    delete membersByTeam[confirmState.team.id]
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

onMounted(loadTeams)
</script>

<template>
  <div class="teams-page">
    <AppHeader eyebrow="Diario de PokéBuilder" :title="`Hola, ${state.user?.username || 'entrenador'}`">
      <template #actions>
        <AppButton type="button" variant="white" @click="openCreateModal">+ Crear equipo</AppButton>
      </template>
    </AppHeader>

    <main class="teams-page__main">
      <div class="teams-page__toolbar">
        <h2 class="teams-page__section-title">Tus equipos</h2>
        <p class="teams-page__section-subtitle">Arma, ajusta y organiza tus builds competitivos.</p>
      </div>

      <p v-if="loadError" class="form-banner" role="alert">{{ loadError }}</p>

      <div v-if="loading" class="teams-page__state">Cargando tus equipos…</div>

      <div v-else-if="teams.length === 0" class="teams-empty">
        <p class="teams-empty__title">Todavía no tienes equipos</p>
        <p class="teams-empty__body">Crea el primero para empezar a planear tu estrategia.</p>
        <AppButton type="button" @click="openCreateModal">Crear mi primer equipo</AppButton>
      </div>

      <div v-else class="teams-list">
        <TeamListItem
          v-for="team in teams"
          :key="team.id"
          :team="team"
          :members="membersByTeam[team.id] || []"
          :members-loading="membersByTeam[team.id] === undefined"
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

.teams-page__main {
  flex: 1;
  width: 100%;
  max-width: 880px;
  margin: 0 auto;
  padding: 32px 40px 64px;
}

.teams-page__toolbar {
  margin-bottom: 24px;
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

.teams-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (max-width: 640px) {
  .teams-page__main {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>
