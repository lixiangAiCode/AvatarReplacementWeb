import { createRouter, createWebHistory } from 'vue-router'
import AvatarReplace from '../views/AvatarReplace.vue'
import PrivacyPolicy from '../views/PrivacyPolicy.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: AvatarReplace
    },
    {
      path: '/privacy-policy',
      name: 'privacy-policy',
      component: PrivacyPolicy
    }
  ]
})

export default router