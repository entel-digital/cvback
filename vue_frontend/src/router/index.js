import { createRouter, createWebHashHistory } from 'vue-router'
import { useUserStore } from '@/stores/user.js'

import SingIngView from '@/views/SingInView.vue'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: SingIngView
    },
    {
      path: '/dashboard',
      name: 'home',
      component: HomeView,
      beforeEnter: async (to, from, next) => {
        const statusSession = await useUserStore().GET_SESSION()
        if (statusSession?.is_authenticated) {
          next()
        } else {
          next({ name: 'login' })
        }
      }
    }
  ]
})

export default router
