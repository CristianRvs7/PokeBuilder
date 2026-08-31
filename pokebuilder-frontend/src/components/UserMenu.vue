<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  user: { type: Object, default: null },
})
const emit = defineEmits(['edit-profile', 'logout'])

const open = ref(false)

const initial = computed(() => {
  const name = props.user?.username || ''
  return name ? name.charAt(0).toUpperCase() : '?'
})

function toggle() {
  open.value = !open.value
}

function handleEdit() {
  open.value = false
  emit('edit-profile')
}

function handleLogout() {
  open.value = false
  emit('logout')
}
</script>

<template>
  <div class="user-menu">
    <button
      type="button"
      class="user-menu__trigger"
      :aria-expanded="open"
      aria-haspopup="true"
      @click="toggle"
    >
      <span class="user-menu__avatar">{{ initial }}</span>
    </button>

    <template v-if="open">
      <div class="user-menu__scrim" @click="open = false"></div>
      <div class="user-menu__panel" role="menu">
        <div class="user-menu__identity">
          <p class="user-menu__name">{{ user?.username || 'Entrenador' }}</p>
          <p class="user-menu__email">{{ user?.email || '' }}</p>
        </div>
        <button type="button" class="user-menu__item" role="menuitem" @click="handleEdit">
          Editar perfil
        </button>
        <button
          type="button"
          class="user-menu__item user-menu__item--danger"
          role="menuitem"
          @click="handleLogout"
        >
          Cerrar sesión
        </button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.user-menu {
  position: relative;
}

.user-menu__trigger {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: none;
  background: #ffffff;
  box-shadow: 0 4px 14px -6px rgba(20, 30, 45, 0.4);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease;
}

.user-menu__trigger:hover {
  transform: scale(1.05);
}

.user-menu__trigger:focus-visible {
  outline: 2px solid #ffffff;
  outline-offset: 2px;
}

.user-menu__avatar {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 15px;
  color: var(--color-mint);
}

.user-menu__scrim {
  position: fixed;
  inset: 0;
  z-index: 60;
}

.user-menu__panel {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  z-index: 61;
  min-width: 220px;
  background: var(--color-panel-raised);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: 0 20px 40px -18px rgba(20, 30, 45, 0.45);
  padding: 8px;
  display: flex;
  flex-direction: column;
}

.user-menu__identity {
  padding: 10px 12px 12px;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 6px;
}

.user-menu__name {
  margin: 0;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 15px;
  color: var(--color-text);
}

.user-menu__email {
  margin: 2px 0 0;
  font-size: 12.5px;
  color: var(--color-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-menu__item {
  border: none;
  background: transparent;
  text-align: left;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-weight: 700;
  font-size: 13.5px;
  color: var(--color-text);
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

.user-menu__item:hover {
  background: rgba(63, 125, 88, 0.1);
  color: var(--color-mint);
}

.user-menu__item--danger:hover {
  background: rgba(193, 71, 58, 0.1);
  color: var(--color-coral);
}
</style>
