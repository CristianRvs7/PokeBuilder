<script setup>
import { computed } from 'vue'

const props = defineProps({
  slotNumber: { type: Number, required: true },
  member: { type: Object, default: null },
})
defineEmits(['add', 'select'])

const spriteUrl = computed(() => {
  if (!props.member) return ''
  return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${props.member.pokemon_id}.png`
})

const displayName = computed(() => {
  if (!props.member) return ''
  const name = props.member.pokemon_name
  return name.charAt(0).toUpperCase() + name.slice(1)
})
</script>

<template>
  <button
    type="button"
    class="roster-slot"
    :class="{ 'roster-slot--filled': !!member }"
    @click="member ? $emit('select') : $emit('add')"
  >
    <span class="roster-slot__circle">
      <img v-if="member" :src="spriteUrl" :alt="displayName" class="roster-slot__sprite" />
      <span v-else class="roster-slot__plus" aria-hidden="true">+</span>
    </span>
    <span class="roster-slot__label">{{ member ? displayName : `Espacio ${slotNumber}` }}</span>
  </button>
</template>

<style scoped>
.roster-slot {
  all: unset;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 100%;
  cursor: pointer;
  padding: 4px;
  border-radius: var(--radius-md);
  transition: background 0.15s ease;
}

.roster-slot:hover {
  background: rgba(63, 125, 88, 0.08);
}

.roster-slot:focus-visible {
  outline: 2px solid var(--color-mint);
  outline-offset: 2px;
}

.roster-slot__circle {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 50%;
  border: 1.5px dashed var(--color-border);
  background: var(--color-paper);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: border-color 0.15s ease, background 0.15s ease;
}

.roster-slot--filled .roster-slot__circle {
  border: 1.5px solid var(--color-border);
  background: var(--color-panel-raised);
}

.roster-slot:hover .roster-slot__circle {
  border-color: var(--color-mint);
}

.roster-slot__plus {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-muted);
}

.roster-slot__sprite {
  width: 86%;
  height: 86%;
  object-fit: contain;
  image-rendering: pixelated;
}

.roster-slot__label {
  font-size: 11.5px;
  font-weight: 700;
  color: var(--color-text-muted);
  text-align: center;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.roster-slot--filled .roster-slot__label {
  color: var(--color-text);
}
</style>
