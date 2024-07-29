import { createRouter, createWebHashHistory } from 'vue-router'
import SingIngView from '@/views/SingInView.vue'
import HomeView from '@/views/HomeView.vue'


const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: '/',
      name: 'login',
      component: SingIngView,
    },
    {
      path: '/dashboard',
      name: 'home',
      component: HomeView,
      children: [
        {
          path: '/abut',
          name: 'abaout',
          component: () => ('@/views/AboutView.vue')
        }
      ]
    }
  ]
})

export default router
