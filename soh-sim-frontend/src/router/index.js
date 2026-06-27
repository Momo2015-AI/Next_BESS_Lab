import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../components/HomePage.vue'),
  },
  {
    path: '/phase1',
    name: 'phase1',
    component: () => import('../pages/Phase1Page.vue'),
  },
  {
    path: '/phase2',
    name: 'phase2',
    component: () => import('../pages/Phase2Page.vue'),
  },
  {
    path: '/phase3',
    name: 'phase3',
    component: () => import('../pages/Phase3Page.vue'),
  },
  {
    path: '/phase4',
    name: 'phase4',
    component: () => import('../pages/Phase4Page.vue'),
  },
  {
    path: '/phase5',
    name: 'phase5',
    component: () => import('../pages/Phase5Page.vue'),
  },
  {
    path: '/survey',
    name: 'survey',
    component: () => import('../pages/SurveyPage.vue'),
  },
  {
    path: '/survey/:id',
    name: 'survey-edit',
    component: () => import('../pages/SurveyPage.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
