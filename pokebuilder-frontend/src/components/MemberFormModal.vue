<script setup>
import { computed, reactive, ref } from 'vue'
import ModalBase from './ModalBase.vue'
import AppInput from './AppInput.vue'
import AppButton from './AppButton.vue'
import { searchPokemon } from '../services/api.js'

const props = defineProps({
  mode: { type: String, default: 'create' }, // create | edit
  slotNumber: { type: Number, required: true },
  member: { type: Object, default: null },
  saving: { type: Boolean, default: false },
  error: { type: String, default: '' },
})
const emit = defineEmits(['submit', 'remove', 'close'])

const NATURES = [
  'Hardy', 'Lonely', 'Brave', 'Adamant', 'Naughty',
  'Bold', 'Docile', 'Relaxed', 'Impish', 'Lax',
  'Timid', 'Hasty', 'Serious', 'Jolly', 'Naive',
  'Modest', 'Mild', 'Quiet', 'Bashful', 'Rash',
  'Calm', 'Gentle', 'Sassy', 'Careful', 'Quirky',
]

const TERA_TYPES = [
  'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison', 'Ground',
  'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy', 'Stellar',
]

function titleCase(text) {
  return text
    .split(/[-\s]/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const query = ref(props.member?.pokemon_name || '')
const searching = ref(false)
const searchError = ref('')
const pokemon = ref(null) // { id, name, types, abilities, sprite }

const form = reactive({
  ability: props.member?.ability || '',
  item: props.member?.item || '',
  nature: props.member?.nature || '',
  tera_type: props.member?.tera_type ? titleCase(props.member.tera_type) : '',
})
const localError = ref('')

async function runSearch() {
  const term = query.value.trim()
  if (!term) return
  searching.value = true
  searchError.value = ''
  localError.value = ''
  try {
    pokemon.value = await searchPokemon(term)
    if (props.mode === 'create' && !form.ability && pokemon.value.abilities?.length) {
      form.ability = titleCase(pokemon.value.abilities[0])
    }
  } catch (err) {
    pokemon.value = null
    searchError.value = err.detail || 'No encontramos ese Pokémon.'
  } finally {
    searching.value = false
  }
}

// En modo edición precargamos la info del Pokémon que ya está en el equipo.
if (props.mode === 'edit' && props.member) {
  runSearch()
}

function handleSubmit() {
  if (!pokemon.value) {
    localError.value = 'Busca un Pokémon primero.'
    return
  }
  const payload = {
    ability: form.ability.trim() || null,
    item: form.item.trim() || null,
    nature: form.nature || null,
    tera_type: form.tera_type ? form.tera_type.toLowerCase() : null,
  }
  if (props.mode === 'create') {
    payload.pokemon_name = pokemon.value.name
    payload.slot = props.slotNumber
  }
  emit('submit', payload)
}

const spriteUrl = computed(() => pokemon.value?.sprite || '')
</script>

<template>
  <ModalBase @close="$emit('close')">
    <p class="modal-eyebrow">{{ mode === 'create' ? `Espacio ${slotNumber}` : 'Editar Pokémon' }}</p>
    <h2 class="modal-title">
      {{ mode === 'create' ? 'Agrega un Pokémon' : 'Ajusta este Pokémon' }}
    </h2>

    <div class="member-form">
      <p v-if="error" class="form-banner" role="alert">{{ error }}</p>

      <div v-if="mode === 'create'" class="member-search">
        <AppInput
          v-model="query"
          label="Pokémon"
          hint="Nombre o número de Pokédex (ej. pikachu, 6)"
          :error="localError"
          @keyup.enter.prevent="runSearch"
        />
        <AppButton type="button" variant="ghost" :loading="searching" @click="runSearch">
          Buscar
        </AppButton>
      </div>
      <div v-else-if="searching" class="member-search__state">Cargando Pokémon…</div>

      <p v-if="searchError" class="form-banner" role="alert">{{ searchError }}</p>

      <div v-if="pokemon" class="member-preview">
        <img :src="spriteUrl" :alt="pokemon.name" class="member-preview__sprite" />
        <div class="member-preview__info">
          <p class="member-preview__name">{{ titleCase(pokemon.name) }}</p>
          <div class="member-preview__types">
            <span v-for="type in pokemon.types" :key="type" class="member-preview__type">
              {{ titleCase(type) }}
            </span>
          </div>
        </div>
      </div>

      <form v-if="pokemon" class="auth-form" novalidate @submit.prevent="handleSubmit">
        <label class="field">
          <span class="field__label">Habilidad</span>
          <select v-model="form.ability" class="field__select">
            <option value="">Sin definir</option>
            <option v-for="ability in pokemon.abilities" :key="ability" :value="titleCase(ability)">
              {{ titleCase(ability) }}
            </option>
          </select>
        </label>

        <AppInput v-model="form.item" label="Objeto" hint="Ej. Leftovers, Choice Scarf" />

        <label class="field">
          <span class="field__label">Naturaleza</span>
          <select v-model="form.nature" class="field__select">
            <option value="">Sin definir</option>
            <option v-for="nature in NATURES" :key="nature" :value="nature">{{ nature }}</option>
          </select>
        </label>

        <label class="field">
          <span class="field__label">Tipo Tera</span>
          <select v-model="form.tera_type" class="field__select">
            <option value="">Sin definir</option>
            <option v-for="type in TERA_TYPES" :key="type" :value="type">{{ type }}</option>
          </select>
        </label>

        <div class="modal-actions">
          <AppButton type="button" variant="ghost" @click="$emit('close')">Cancelar</AppButton>
          <AppButton :loading="saving">
            {{ mode === 'create' ? 'Agregar al equipo' : 'Guardar cambios' }}
          </AppButton>
        </div>
      </form>

      <div v-if="mode === 'edit'" class="member-danger">
        <button type="button" class="member-danger__btn" @click="$emit('remove')">
          Quitar del equipo
        </button>
      </div>
    </div>
  </ModalBase>
</template>

<style scoped>
.member-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.member-search {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.member-search .field {
  flex: 1;
}

.member-search .btn {
  width: auto;
  margin-bottom: 2px;
}

.member-search__state {
  color: var(--color-text-muted);
  font-size: 13.5px;
}

.member-preview {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  border-radius: var(--radius-md);
  background: var(--color-paper);
  border: 1px solid var(--color-border);
}

.member-preview__sprite {
  width: 56px;
  height: 56px;
  object-fit: contain;
  image-rendering: pixelated;
  flex-shrink: 0;
}

.member-preview__name {
  margin: 0 0 6px;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 16px;
}

.member-preview__types {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.member-preview__type {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 10.5px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--color-mint);
  background: rgba(63, 125, 88, 0.12);
  padding: 3px 9px;
  border-radius: var(--radius-pill);
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-align: left;
}

.field__label {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}

.field__select {
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  font-family: var(--font-body);
  font-size: 15px;
  padding: 8px 2px;
  outline: none;
  transition: border-color 0.2s ease;
}

.field__select:focus-visible {
  outline: 2px solid var(--color-mint);
  outline-offset: 2px;
}

.member-danger {
  border-top: 1px solid var(--color-border);
  padding-top: 14px;
  text-align: center;
}

.member-danger__btn {
  border: none;
  background: transparent;
  color: var(--color-coral);
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 13.5px;
  cursor: pointer;
}

.member-danger__btn:hover {
  text-decoration: underline;
}
</style>
