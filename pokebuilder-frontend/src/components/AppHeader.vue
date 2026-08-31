<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../stores/auth.js'
import { updateCurrentUser } from '../services/api.js'
import UserMenu from './UserMenu.vue'
import EditProfileModal from './EditProfileModal.vue'

defineProps({
  eyebrow: { type: String, default: '' },
  title: { type: String, default: '' },
  showBack: { type: Boolean, default: false },
})

const router = useRouter()
const { state, clearSession, updateUser } = useAuth()

const editProfileModal = reactive({ open: false, saving: false, error: '' })

function goBack() {
  router.push('/')
}

function openEditProfile() {
  editProfileModal.error = ''
  editProfileModal.open = true
}

async function handleEditProfileSubmit(payload) {
  editProfileModal.saving = true
  editProfileModal.error = ''
  try {
    const updated = await updateCurrentUser(state.token, payload)
    updateUser(updated)
    editProfileModal.open = false
  } catch (err) {
    editProfileModal.error = err.detail || 'No pudimos guardar los cambios.'
  } finally {
    editProfileModal.saving = false
  }
}

function handleLogout() {
  clearSession()
  router.push('/login')
}
</script>

<template>
  <header class="app-header">
    <div class="app-header__visual" aria-hidden="true">
      <div class="app-header__bg"></div>
      <div class="app-header__scrim"></div>
    </div>

    <div class="app-header__content">
      <div class="app-header__left">
        <button v-if="showBack" type="button" class="app-header__back" aria-label="Volver" @click="goBack">
          ←
        </button>
        <div class="app-header__text">
          <p v-if="eyebrow" class="app-header__eyebrow">{{ eyebrow }}</p>
          <h1 class="app-header__title">{{ title }}</h1>
        </div>
      </div>

      <div class="app-header__right">
        <slot name="actions" />
        <UserMenu :user="state.user" @edit-profile="openEditProfile" @logout="handleLogout" />
      </div>
    </div>
  </header>

  <EditProfileModal
    v-if="editProfileModal.open"
    :user="state.user"
    :saving="editProfileModal.saving"
    :error="editProfileModal.error"
    @submit="handleEditProfileSubmit"
    @close="editProfileModal.open = false"
  />
</template>

<style scoped>
.app-header {
  position: relative;
}

.app-header__visual {
  position: absolute;
  inset: 0;
  overflow: hidden;
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  box-shadow: 0 16px 32px -22px rgba(20, 30, 45, 0.55);
}

.app-header__bg {
  position: absolute;
  inset: 0;
  background-image: url('../assets/header-bg.jpg');
  background-size: cover;
  background-position: center 42%;
}

.app-header__scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(18, 28, 42, 0.4), rgba(18, 28, 42, 0.32));
}

.app-header__content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 26px 40px;
  min-height: 116px;
}

.app-header__left {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
}

.app-header__back {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #ffffff;
  color: var(--color-mint);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 14px -6px rgba(20, 30, 45, 0.4);
  transition: transform 0.15s ease;
}

.app-header__back:hover {
  transform: translateX(-2px);
}

.app-header__text {
  min-width: 0;
}

.app-header__eyebrow {
  margin: 0 0 4px;
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #ffffff;
  opacity: 0.85;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
}

.app-header__title {
  margin: 0;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 22px;
  color: #ffffff;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.35);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.app-header__right {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-header__right :deep(.btn) {
  width: auto;
}

@media (max-width: 640px) {
  .app-header__content {
    padding: 20px 20px;
    min-height: 96px;
  }

  .app-header__title {
    font-size: 18px;
    max-width: 46vw;
  }

  .app-header__right :deep(.btn) {
    padding: 10px 14px;
    font-size: 13px;
  }
}
</style>
