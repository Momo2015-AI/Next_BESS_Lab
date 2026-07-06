import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../components/HomePage.vue')
  },
  {
    path: '/phase1',
    name: 'phase1',
    component: () => import('../pages/Phase1Page.vue')
  },
  {
    path: '/phase2',
    name: 'phase2',
    component: () => import('../pages/Phase2Page.vue')
  },
  {
    path: '/phase3',
    name: 'phase3',
    component: () => import('../pages/Phase3Page.vue')
  },
  {
    path: '/phase4',
    name: 'phase4',
    component: () => import('../pages/Phase4Page.vue')
  },
  {
    path: '/phase5',
    name: 'phase5',
    component: () => import('../pages/Phase5Page.vue')
  },
  {
    path: '/survey',
    name: 'survey',
    component: () => import('../pages/SurveyPage.vue')
  },
  {
    path: '/survey/:id',
    name: 'survey-edit',
    component: () => import('../pages/SurveyPage.vue')
  },
  {
    path: '/tools/formula',
    name: 'tool-formula',
    component: () => import('../pages/ToolFormulaPage.vue')
  },
  {
    path: '/tools/auxpower',
    name: 'tool-auxpower',
    component: () => import('../pages/ToolAuxPowerPage.vue')
  },
  {
    path: '/tools/engineering',
    name: 'tool-engineering',
    component: () => import('../pages/ToolEngineeringPage.vue')
  },
  {
    path: '/tools/datainject',
    name: 'tool-datainject',
    component: () => import('../pages/ToolDataInjectPage.vue')
  },
  {
    path: '/tools/conditions',
    name: 'tool-conditions',
    component: () => import('../pages/ToolConditionsPage.vue')
  },
  {
    path: '/tools/params',
    name: 'tool-params',
    component: () => import('../pages/ToolParamsPage.vue')
  },
  {
    path: '/tools/financial',
    name: 'tool-financial',
    component: () => import('../pages/ToolFinancialPage.vue')
  },
  {
    path: '/tools/config',
    name: 'tool-config',
    component: () => import('../pages/ToolConfigPage.vue')
  },
  {
    path: '/tools/survey-view',
    name: 'tool-survey-view',
    component: () => import('../pages/ToolSurveyViewPage.vue')
  },
  {
    path: '/tools/simulation-view',
    name: 'tool-simulation-view',
    component: () => import('../pages/ToolSimulationViewPage.vue')
  },
  {
    path: '/tools/report',
    name: 'tool-report',
    component: () => import('../pages/ToolReportPage.vue')
  },
  {
    path: '/tools/projects',
    name: 'tool-projects',
    component: () => import('../pages/ToolProjectsPage.vue')
  },
  {
    path: '/tools/templates',
    name: 'tool-templates',
    component: () => import('../pages/ToolTemplatesPage.vue')
  },
  {
    path: '/tools/rules',
    name: 'tool-rules',
    component: () => import('../pages/ToolRulesPage.vue')
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import('../pages/AuthPage.vue')
  },
  {
    path: '/epc',
    name: 'epc',
    component: () => import('../pages/EpcPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const protectedRoutes = ['phase1', 'phase2', 'phase3', 'phase4', 'phase5', 'survey', 'epc']

router.beforeEach((to, from, next) => {
  if (protectedRoutes.includes(to.name)) {
    const token = sessionStorage.getItem('auth_token')
    if (!token) {
      next({ name: 'home' })
      return
    }
  }
  next()
})

export default router
