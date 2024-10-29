import { createRouter, createWebHashHistory } from 'vue-router'
import { useUserStore } from '@/stores/user.js'

import ResetPasswordView from '@/views/ResetPasswordView.vue'
import SingIngView from '@/views/SingInView.vue'
import HomeView from '@/views/HomeView.vue'
import EventView from '@/views/EventView.vue'
import { event } from 'quasar'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      props: true,
      component: SingIngView
    },
    {
      path: '/account/password/reset/key/:key',
      name: 'reset',
      props: true,
      component: ResetPasswordView
    },
    {
      path: '/dashboard/:eventId?/:dateRange?/:label?',
      name: 'home',
      props: true,
      component: HomeView,
      beforeEnter: async (to, from, next) => {
        const statusSession = await useUserStore().GET_SESSION()
        if (statusSession?.meta.is_authenticated) {
          next()
        } else {
          next({ name: 'login' })
        }
      }
    },
    
    {
      path: '/?token=:token&eventid=:eventid',
      name: 'event',
      props: true,
      component: EventView,
      beforeEnter: async (to, from, next) => {
        const statusSession = await useUserStore().GET_SESSION()
        if (statusSession?.meta.is_authenticated) {
          next()
        } else {
          const tokenSession = await useUserStore().TOKEN_SESSION(to.params.token)
          if (tokenSession.status === 200) {
            next()
          } else {
            next({ name: 'login' })
          }
        }
      }
    }
  ]
})

export default router
