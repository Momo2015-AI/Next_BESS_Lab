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
  {
    path: '/tools/formula',
    name: 'tool-formula',
    component: () => import('../pages/ToolFormulaPage.vue'),
  },
  {
    path: '/tools/auxpower',
    name: 'tool-auxpower',
    component: () => import('../pages/ToolAuxPowerPage.vue'),
  },
  {
    path: '/tools/engineering',
    name: 'tool-engineering',
    component: () => import('../pages/ToolEngineeringPage.vue'),
  },
  {
    path: '/tools/datainject',
    name: 'tool-datainject',
    component: () => import('../pages/ToolDataInjectPage.vue'),
  },
  {
    path: '/tools/conditions',
    name: 'tool-conditions',
    component: () => import('../pages/ToolConditionsPage.vue'),
  },
  {
    path: '/tools/params',
    name: 'tool-params',
    component: () => import('../pages/ToolParamsPage.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
