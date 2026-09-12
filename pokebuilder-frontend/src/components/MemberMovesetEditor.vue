<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import AppInput from './AppInput.vue'
import { assignMoveToMember, fetchLearnableMoves, fetchMemberWithMoves } from '../services/api.js'
import { useAuth } from '../stores/auth.js'

const props = defineProps({
  teamId: { type: [String, Number], required: true },
  member: { type: Object, required: true }, // necesita id y pokemon_name
})

const { state } = useAuth()

function titleCase(text) {
  return text
    .split(/[-\s]/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const DAMAGE_CLASS_LABEL = {
  physical: 'Físico',
  special: 'Especial',
  status: 'Estado',
}

const loading = ref(true)
const loadError = ref('')
const learnableMoves = ref([]) // MoveFullResponse[]
const slots = ref([null, null, null, null]) // objeto movimiento o null por slot

const picker = reactive({ open: false, slot: null, query: '', assigning: false, error: '' })

async function loadMoveset() {
  loading.value = true
  loadError.value = ''
  try {
    const [moves, memberFull] = await Promise.all([
      fetchLearnableMoves(props.member.pokemon_name),
      fetchMemberWithMoves(state.token, props.teamId, props.member.pokemon_name),
    ])
    learnableMoves.value = moves
    slots.value = [1, 2, 3, 4].map((slotNumber) => {
      const name = memberFull?.[`movslot${slotNumber}`]
      if (!name) return null
      // movslot llega solo con el nombre; lo cruzamos con el movepool para
      // obtener tipo/poder/clase de daño y poder mostrarlo con más detalle.
      return moves.find((m) => m.name === name) || { name }
    })
  } catch (err) {
    loadError.value = err.detail || 'No pudimos cargar los movimientos de este Pokémon.'
  } finally {
    loading.value = false
  }
}

const assignedIds = computed(() => new Set(slots.value.filter(Boolean).map((m) => m.id).filter(Boolean)))

const filteredMoves = computed(() => {
  const term = picker.query.trim().toLowerCase()
  return learnableMoves.value
    .filter((m) => !assignedIds.value.has(m.id))
    .filter((m) => !term || m.name.replace('-', ' ').toLowerCase().includes(term))
    .slice(0, 30)
})

function openPicker(slotNumber) {
  picker.open = true
  picker.slot = slotNumber
  picker.query = ''
  picker.error = ''
}

function closePicker() {
  picker.open = false
  picker.slot = null
}

async function pickMove(move) {
  picker.assigning = true
  picker.error = ''
  try {
    await assignMoveToMember(state.token, {
      team_member_id: props.member.id,
      move_id: move.id,
      slot: picker.slot,
    })
    slots.value[picker.slot - 1] = move
    closePicker()
  } catch (err) {
    picker.error = err.detail || 'No pudimos asignar ese movimiento.'
  } finally {
    picker.assigning = false
  }
}

onMounted(loadMoveset)
</script>

<template>
  <div class="moveset">
    <p class="moveset__label">Movimientos</p>

    <p v-if="loadError" class="form-banner" role="alert">{{ loadError }}</p>
    <p v-else-if="loading" class="moveset__state">Cargando movimientos…</p>

    <div v-else class="moveset__grid">
      <div v-for="slotNumber in [1, 2, 3, 4]" :key="slotNumber" class="move-slot">
        <template v-if="slots[slotNumber - 1]">
          <div class="move-slot__filled" :class="`move-slot__filled--${slots[slotNumber - 1].damage_class || 'status'}`">
            <span class="move-slot__name">{{ titleCase(slots[slotNumber - 1].name) }}</span>
            <span v-if="slots[slotNumber - 1].type" class="move-slot__type">
              {{ titleCase(slots[slotNumber - 1].type) }}
            </span>
            <span v-if="slots[slotNumber - 1].power != null" class="move-slot__power">
              Poder {{ slots[slotNumber - 1].power }}
            </span>
          </div>
        </template>
        <button v-else type="button" class="move-slot__empty" @click="openPicker(slotNumber)">
          <span aria-hidden="true">+</span>
          <span>Espacio {{ slotNumber }}</span>
        </button>
      </div>
    </div>

    <p v-if="!loading && !loadError && slots.every((s) => s)" class="moveset__hint">
      Este Pokémon ya tiene sus 4 movimientos asignados.
    </p>

    <div v-if="picker.open" class="move-picker">
      <AppInput v-model="picker.query" label="Buscar movimiento" hint="Solo se muestran los que puede aprender" />
      <p v-if="picker.error" class="form-banner" role="alert">{{ picker.error }}</p>
      <p v-if="!filteredMoves.length" class="moveset__state">Sin resultados.</p>
      <ul v-else class="move-picker__list">
        <li v-for="move in filteredMoves" :key="move.id">
          <button
            type="button"
            class="move-picker__option"
            :disabled="picker.assigning"
            @click="pickMove(move)"
          >
            <span class="move-picker__option-name">{{ titleCase(move.name) }}</span>
            <span class="move-picker__option-meta">
              {{ titleCase(move.type) }} · {{ DAMAGE_CLASS_LABEL[move.damage_class] || move.damage_class }}
            </span>
          </button>
        </li>
      </ul>
      <button type="button" class="move-picker__cancel" @click="closePicker">Cancelar</button>
    </div>
  </div>
</template>

<style scoped>
.moveset {
  border-top: 1px solid var(--color-border);
  padding-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.moveset__label {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin: 0;
}

.moveset__state {
  color: var(--color-text-muted);
  font-size: 13.5px;
  margin: 0;
}

.moveset__hint {
  color: var(--color-text-muted);
  font-size: 12.5px;
  margin: 0;
}

.moveset__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.move-slot__empty {
  all: unset;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  border: 1.5px dashed var(--color-border);
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease;
}

.move-slot__empty:hover {
  border-color: var(--color-mint);
  color: var(--color-mint);
}

.move-slot__filled {
  padding: 10px 12px;
  border-radius: var(--radius-md);
  background: var(--color-paper);
  border: 1px solid var(--color-border);
  border-left: 4px solid var(--color-text-muted);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.move-slot__filled--physical {
  border-left-color: var(--color-coral);
}

.move-slot__filled--special {
  border-left-color: var(--color-sky-top);
}

.move-slot__filled--status {
  border-left-color: var(--color-text-muted);
}

.move-slot__name {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 13.5px;
}

.move-slot__type {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 10px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--color-mint);
}

.move-slot__power {
  font-size: 11.5px;
  color: var(--color-text-muted);
}

.move-picker {
  background: var(--color-panel-raised);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.move-picker__list {
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: 200px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.move-picker__option {
  all: unset;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 2px;
  width: 100%;
  padding: 8px 10px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.15s ease;
}

.move-picker__option:hover:not(:disabled) {
  background: rgba(63, 125, 88, 0.1);
}

.move-picker__option:disabled {
  opacity: 0.6;
  cursor: progress;
}

.move-picker__option-name {
  font-weight: 700;
  font-size: 13.5px;
}

.move-picker__option-meta {
  font-size: 11.5px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.move-picker__cancel {
  align-self: flex-start;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  font-weight: 700;
  font-size: 12.5px;
  cursor: pointer;
}

.move-picker__cancel:hover {
  text-decoration: underline;
}
</style>
