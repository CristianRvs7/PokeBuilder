import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import TeamsView from '../views/TeamsView.vue'
import TeamDetailView from '../views/TeamDetailView.vue'
import { useAuth } from '../stores/auth.js'

const routes = [
  { path: '/', name: 'teams', component: TeamsView, meta: { requiresAuth: true } },
  { path: '/teams/:id', name: 'team-detail', component: TeamDetailView, meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },
  { path: '/register', name: 'register', component: RegisterView, meta: { guestOnly: true } },
  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const { isAuthenticated } = useAuth()
  const authed = isAuthenticated()

  if (to.meta.requiresAuth && !authed) {
    return { name: 'login' }
  }
  if (to.meta.guestOnly && authed) {
    return { name: 'teams' }
  }
  return true
})

export default router
