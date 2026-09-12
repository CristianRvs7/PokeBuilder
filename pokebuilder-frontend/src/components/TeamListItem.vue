<script setup>
import { computed } from 'vue'

const props = defineProps({
  team: { type: Object, required: true },
  members: { type: Array, default: () => [] },
})
defineEmits(['open', 'edit', 'delete'])

const sortedMembers = computed(() => [...props.members].sort((a, b) => a.slot - b.slot).slice(0, 6))

function spriteUrl(member) {
  return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${member.pokemon_id}.png`
}
</script>

<template>
  <article class="team-row">
    <button type="button" class="team-row__body" @click="$emit('open')">
      <div class="team-row__sprites">
        <template v-if="sortedMembers.length">
          <span
            v-for="(member, index) in sortedMembers"
            :key="member.id"
            class="team-row__sprite"
            :style="{ zIndex: index + 1 }"
          >
            <img :src="spriteUrl(member)" :alt="member.pokemon_name" />
          </span>
        </template>
        <span v-else class="team-row__sprite team-row__sprite--empty" aria-hidden="true"></span>
      </div>

      <div class="team-row__info">
        <div class="team-row__title-line">
          <span v-if="team.format" class="team-row__format">{{ team.format }}</span>
          <h3 class="team-row__name">{{ team.team_name }}</h3>
        </div>
        <p class="team-row__description">{{ team.description || 'Sin descripción todavía.' }}</p>
      </div>

      <span class="team-row__count">{{ members.length }}/6</span>
    </button>

    <div class="team-row__actions">
      <button type="button" class="team-row__action" @click="$emit('edit')">Editar</button>
      <button type="button" class="team-row__action team-row__action--danger" @click="$emit('delete')">
        Eliminar
      </button>
    </div>
  </article>
</template>

<style scoped>
.team-row {
  display: flex;
  align-items: stretch;
  background: var(--color-panel-raised);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: 0 10px 24px -20px rgba(43, 33, 24, 0.4);
  overflow: hidden;
}

.team-row__body {
  all: unset;
  box-sizing: border-box;
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  cursor: pointer;
  text-align: left;
}

.team-row__body:hover .team-row__name {
  color: var(--color-mint);
}

.team-row__body:focus-visible {
  outline: 2px solid var(--color-mint);
  outline-offset: -2px;
}

.team-row__sprites {
  flex-shrink: 0;
  display: flex;
}

.team-row__sprite {
  position: relative;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--color-paper);
  border: 2px solid var(--color-panel-raised);
  margin-left: -12px;
}

.team-row__sprite:first-child {
  margin-left: 0;
}

.team-row__sprite img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  image-rendering: pixelated;
}

.team-row__sprite--empty {
  border-style: dashed;
  border-color: var(--color-border);
  background: var(--color-paper);
}

.team-row__info {
  flex: 1;
  min-width: 0;
}

.team-row__title-line {
  display: flex;
  align-items: baseline;
  gap: 10px;
  flex-wrap: wrap;
}

.team-row__format {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 10.5px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-mint);
  background: rgba(63, 125, 88, 0.12);
  padding: 3px 9px;
  border-radius: var(--radius-pill);
}

.team-row__name {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 17px;
  margin: 0;
  color: var(--color-text);
  transition: color 0.15s ease;
}

.team-row__description {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--color-text-muted);
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.team-row__count {
  flex-shrink: 0;
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 12.5px;
  color: var(--color-text-muted);
  background: var(--color-paper);
  padding: 4px 10px;
  border-radius: var(--radius-pill);
}

.team-row__actions {
  display: flex;
  flex-direction: column;
  border-left: 1px solid var(--color-border);
}

.team-row__action {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0 16px;
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 12.5px;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

.team-row__action:first-child {
  border-bottom: 1px solid var(--color-border);
}

.team-row__action:hover {
  background: rgba(63, 125, 88, 0.08);
  color: var(--color-mint);
}

.team-row__action--danger:hover {
  background: rgba(193, 71, 58, 0.08);
  color: var(--color-coral);
}

@media (max-width: 640px) {
  .team-row__body {
    flex-wrap: wrap;
    row-gap: 8px;
  }

  .team-row__count {
    order: 1;
  }

  .team-row__info {
    order: 2;
    flex-basis: 100%;
  }
}
</style>
