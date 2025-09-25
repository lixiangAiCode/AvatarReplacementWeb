import { createRouter, createWebHistory } from 'vue-router'
import AvatarReplace from '../views/AvatarReplace.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: AvatarReplace
    }
  ]
})

export default router