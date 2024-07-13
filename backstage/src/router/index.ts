import { createRouter, createWebHistory } from 'vue-router'
import SystemView from '@/views/SystemView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'System',
      component: SystemView
    },
    {
      path: '/teacher',
      name: 'Teacher',
      component: () => import('@/views/TeacherView.vue')
    },
    {
      path: '/comment',
      name: 'Comment',
      component: () => import('@/views/CommentView.vue')
    },
    {
      path: '/score',
      name: 'Score',
      component: () => import('@/views/ScoreView.vue')
    },
    {
      path: '/script',
      name: 'Script',
      component: () => import('@/views/ScriptView.vue')
    }
  ]
})

export default router
