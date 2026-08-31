<script setup>
defineProps({
  team: { type: Object, required: true },
})
defineEmits(['open', 'edit', 'delete'])
</script>

<template>
  <article class="team-card">
    <button type="button" class="team-card__body" @click="$emit('open')">
      <span v-if="team.format" class="team-card__format">{{ team.format }}</span>
      <h3 class="team-card__name">{{ team.team_name }}</h3>
      <p class="team-card__description">{{ team.description || 'Sin descripción todavía.' }}</p>

      <div class="team-card__roster">
        <div class="team-card__slots" aria-hidden="true">
          <span v-for="n in 6" :key="n" class="team-card__slot"></span>
        </div>
        <span class="team-card__roster-label">Pokémon: próximamente</span>
      </div>
    </button>

    <div class="team-card__actions">
      <button type="button" class="team-card__action" @click="$emit('edit')">Editar</button>
      <button type="button" class="team-card__action team-card__action--danger" @click="$emit('delete')">
        Eliminar
      </button>
    </div>
  </article>
</template>

<style scoped>
.team-card {
  display: flex;
  flex-direction: column;
  background: var(--color-panel-raised);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: 0 18px 40px -28px rgba(43, 33, 24, 0.35);
  overflow: hidden;
}

.team-card__body {
  all: unset;
  box-sizing: border-box;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 22px 22px 18px;
  text-align: left;
}

.team-card__body:hover .team-card__name {
  color: var(--color-mint);
}

.team-card__body:focus-visible {
  outline: 2px solid var(--color-mint);
  outline-offset: -2px;
}

.team-card__format {
  align-self: flex-start;
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-mint);
  background: rgba(63, 125, 88, 0.12);
  padding: 4px 10px;
  border-radius: var(--radius-pill);
}

.team-card__name {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 19px;
  margin: 0;
  color: var(--color-text);
  transition: color 0.15s ease;
}

.team-card__description {
  margin: 0;
  font-size: 13.5px;
  color: var(--color-text-muted);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.team-card__roster {
  margin-top: 6px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.team-card__slots {
  display: flex;
  gap: 7px;
}

.team-card__slot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1.5px dashed var(--color-border);
  background: var(--color-paper);
}

.team-card__roster-label {
  font-size: 11.5px;
  color: var(--color-text-muted);
}

.team-card__actions {
  display: flex;
  border-top: 1px solid var(--color-border);
}

.team-card__action {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px;
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 13px;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

.team-card__action:first-child {
  border-right: 1px solid var(--color-border);
}

.team-card__action:hover {
  background: rgba(63, 125, 88, 0.08);
  color: var(--color-mint);
}

.team-card__action--danger:hover {
  background: rgba(193, 71, 58, 0.08);
  color: var(--color-coral);
}
</style>
