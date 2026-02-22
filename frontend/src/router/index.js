import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from 'src/stores/auth-store'

const routes = [
  {
    path: '/',
    children: [
      { path: '', name: 'Index', component: () => import('pages/IndexPage.vue'), meta: { requiresAuth: true } },
      { path: 'add', name: 'AddOrder', component: () => import('pages/AddOrder.vue'), meta: { requiresAuth: true } },
      { path: 'profile', name: 'Profile', component: () => import('pages/ProfilePage.vue'), meta: { requiresAuth: true } },
      { path: 'orders/:id', name: 'OrderDetail', component: () => import('pages/OrderDetailPage.vue'), meta: { requiresAuth: true } },
      { path: 'login', name: 'Login', component: () => import('pages/LoginPage.vue'), meta: { requiresAuth: false } },
      { path: 'register', name: 'Register', component: () => import('pages/RegisterPage.vue'), meta: { requiresAuth: false } },
    ]
  },
  {
    path: '/:catchAll(.*)*',
    name: 'NotFound',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Проверка авторизации
let initialCheckDone = false
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (!initialCheckDone) {
    initialCheckDone = true
    if (authStore.accessToken) {
      await authStore.getMe()
    }
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if ((to.name === 'Login' || to.name === 'Register') && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
