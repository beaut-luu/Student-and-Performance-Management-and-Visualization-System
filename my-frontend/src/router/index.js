import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue'), meta: { requiresAuth: true } },
  { path: '/profile', name: 'profile', component: () => import('@/views/ProfileView.vue'), meta: { requiresAuth: true } },
  { path: '/activities', name: 'activityList', component: () => import('@/views/ActivityListView.vue'), meta: { requiresAuth: true } },
  { path: '/activity/create', name: 'activityCreate', component: () => import('@/views/ActivityCreateView.vue'), meta: { requiresAuth: true } },
  { path: '/activity/:id', name: 'activityDetail', component: () => import('@/views/ActivityDetailView.vue'), meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },
  { path: '/register', name: 'register', component: () => import('@/views/RegisterView.vue') },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) return { name: 'login' }
  if ((to.name === 'login' || to.name === 'register') && token) return { name: 'home' }
})

export default router
