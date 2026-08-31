<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  addTeamMember,
  deleteTeamMember,
  fetchTeamById,
  fetchTeamMembers,
  updateTeam,
  updateTeamMember,
} from '../services/api.js'
import { useAuth } from '../stores/auth.js'
import AppButton from '../components/AppButton.vue'
import TeamFormModal from '../components/TeamFormModal.vue'
import RosterSlot from '../components/RosterSlot.vue'
import MemberFormModal from '../components/MemberFormModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const route = useRoute()
const { state } = useAuth()
const teamId = route.params.id

const team = ref(null)
const members = ref([])
const loading = ref(true)
const loadError = ref('')

const editing = ref(false)
const saving = ref(false)
const saveError = ref('')

const memberModal = reactive({ open: false, mode: 'create', slotNumber: 1, member: null, saving: false, error: '' })
const confirmState = reactive({ open: false, member: null, busy: false, error: '' })

const slots = computed(() =>
  Array.from({ length: 6 }, (_, i) => {
    const slotNumber = i + 1
    return { slotNumber, member: members.value.find((m) => m.slot === slotNumber) || null }
  }),
)

function capitalize(text) {
  return text ? text.charAt(0).toUpperCase() + text.slice(1) : ''
}

async function loadTeam() {
  loading.value = true
  loadError.value = ''
  try {
    const [teamData, memberData] = await Promise.all([
      fetchTeamById(state.token, teamId),
      fetchTeamMembers(state.token, teamId),
    ])
    team.value = teamData
    members.value = memberData
  } catch (err) {
    loadError.value = err.detail || 'No pudimos cargar este equipo.'
  } finally {
    loading.value = false
  }
}

async function handleSave(payload) {
  saving.value = true
  saveError.value = ''
  try {
    team.value = await updateTeam(state.token, teamId, payload)
    editing.value = false
  } catch (err) {
    saveError.value = err.detail || 'No pudimos guardar los cambios.'
  } finally {
    saving.value = false
  }
}

function openAddMember(slotNumber) {
  memberModal.mode = 'create'
  memberModal.slotNumber = slotNumber
  memberModal.member = null
  memberModal.error = ''
  memberModal.open = true
}

function openEditMember(member) {
  memberModal.mode = 'edit'
  memberModal.slotNumber = member.slot
  memberModal.member = member
  memberModal.error = ''
  memberModal.open = true
}

function closeMemberModal() {
  memberModal.open = false
}

async function handleMemberSubmit(payload) {
  memberModal.saving = true
  memberModal.error = ''
  try {
    if (memberModal.mode === 'create') {
      const created = await addTeamMember(state.token, teamId, payload)
      members.value = [...members.value, created]
    } else {
      const updated = await updateTeamMember(state.token, teamId, memberModal.member.slot, payload)
      members.value = members.value.map((m) => (m.slot === updated.slot ? updated : m))
    }
    memberModal.open = false
  } catch (err) {
    memberModal.error = err.detail || 'No pudimos guardar este Pokémon.'
  } finally {
    memberModal.saving = false
  }
}

function handleRemoveRequest() {
  confirmState.member = memberModal.member
  confirmState.error = ''
  confirmState.open = true
  memberModal.open = false
}

function closeConfirm() {
  confirmState.open = false
}

async function handleConfirmRemove() {
  confirmState.busy = true
  confirmState.error = ''
  try {
    await deleteTeamMember(state.token, teamId, confirmState.member.slot)
    members.value = members.value.filter((m) => m.slot !== confirmState.member.slot)
    confirmState.open = false
  } catch (err) {
    confirmState.error = err.detail || 'No pudimos quitar este Pokémon.'
  } finally {
    confirmState.busy = false
  }
}

onMounted(loadTeam)
</script>

<template>
  <div class="team-detail">
    <div class="team-detail__wrap">
      <router-link to="/" class="team-detail__back">← Volver a mis equipos</router-link>

      <p v-if="loadError" class="form-banner" role="alert">{{ loadError }}</p>
      <div v-else-if="loading" class="team-detail__state">Cargando equipo…</div>

      <div v-else-if="team" class="team-detail__card">
        <div class="team-detail__head">
          <div>
            <span v-if="team.format" class="team-detail__format">{{ team.format }}</span>
            <h1 class="team-detail__name">{{ team.team_name }}</h1>
            <p class="team-detail__description">{{ team.description || 'Sin descripción todavía.' }}</p>
          </div>
          <AppButton type="button" variant="ghost" class="team-detail__edit" @click="editing = true">
            Editar equipo
          </AppButton>
        </div>

        <div class="team-detail__roster">
          <p class="team-detail__roster-eyebrow">Roster · {{ members.length }}/6</p>
          <div class="team-detail__slots">
            <RosterSlot
              v-for="s in slots"
              :key="s.slotNumber"
              :slot-number="s.slotNumber"
              :member="s.member"
              @add="openAddMember(s.slotNumber)"
              @select="openEditMember(s.member)"
            />
          </div>
          <p v-if="members.length === 0" class="team-detail__roster-hint">
            Toca un espacio vacío para agregar tu primer Pokémon.
          </p>
        </div>
      </div>
    </div>

    <TeamFormModal
      v-if="editing"
      mode="edit"
      :team="team"
      :saving="saving"
      :error="saveError"
      @submit="handleSave"
      @close="editing = false"
    />

    <MemberFormModal
      v-if="memberModal.open"
      :mode="memberModal.mode"
      :slot-number="memberModal.slotNumber"
      :member="memberModal.member"
      :saving="memberModal.saving"
      :error="memberModal.error"
      @submit="handleMemberSubmit"
      @remove="handleRemoveRequest"
      @close="closeMemberModal"
    />

    <ConfirmDialog
      v-if="confirmState.open"
      title="¿Quitar este Pokémon?"
      :message="`Vas a quitar a «${capitalize(confirmState.member?.pokemon_name)}» del equipo.`"
      confirm-label="Quitar"
      :busy="confirmState.busy"
      :error="confirmState.error"
      @confirm="handleConfirmRemove"
      @cancel="closeConfirm"
    />
  </div>
</template>

<style scoped>
.team-detail {
  min-height: 100vh;
  display: flex;
  padding: 40px 24px;
}

.team-detail__wrap {
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.team-detail__back {
  color: var(--color-text-muted);
  font-weight: 700;
  font-size: 14px;
  align-self: flex-start;
}

.team-detail__state {
  color: var(--color-text-muted);
  text-align: center;
  padding: 40px 0;
}

.team-detail__card {
  background: var(--color-panel-raised);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: 0 18px 40px -28px rgba(43, 33, 24, 0.35);
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.team-detail__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.team-detail__format {
  display: inline-block;
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-mint);
  background: rgba(63, 125, 88, 0.12);
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  margin-bottom: 10px;
}

.team-detail__name {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 27px;
  margin: 0 0 8px;
}

.team-detail__description {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 14.5px;
  line-height: 1.6;
  max-width: 46ch;
}

.team-detail__edit {
  width: auto;
}

.team-detail__roster {
  border-top: 1px solid var(--color-border);
  padding-top: 24px;
}

.team-detail__roster-eyebrow {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-coral);
  margin: 0 0 14px;
}

.team-detail__slots {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
  max-width: 460px;
}

.team-detail__roster-hint {
  margin: 16px 0 0;
  color: var(--color-text-muted);
  font-size: 13.5px;
  line-height: 1.5;
  max-width: 46ch;
}

@media (max-width: 640px) {
  .team-detail__slots {
    grid-template-columns: repeat(3, 1fr);
    max-width: none;
  }
}
</style>
