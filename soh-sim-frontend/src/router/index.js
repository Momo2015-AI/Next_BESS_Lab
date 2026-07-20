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
    component: () => import('../pages/Phase1Page.vue'),
    meta: { permission: 'phase1' }
  },
  {
    path: '/phase2',
    name: 'phase2',
    component: () => import('../pages/Phase2Page.vue'),
    meta: { permission: 'phase2' }
  },
  {
    path: '/phase3',
    name: 'phase3',
    component: () => import('../pages/Phase3Page.vue'),
    meta: { permission: 'phase3' }
  },
  {
    path: '/phase4',
    name: 'phase4',
    component: () => import('../pages/Phase4Page.vue'),
    meta: { permission: 'phase4' }
  },
  {
    path: '/phase5',
    name: 'phase5',
    component: () => import('../pages/Phase5Page.vue'),
    meta: { permission: 'phase5' }
  },
  {
    path: '/survey',
    name: 'survey',
    component: () => import('../pages/SurveyPage.vue'),
    meta: { permission: 'phase1' }
  },
  {
    path: '/survey/:id',
    name: 'survey-edit',
    component: () => import('../pages/SurveyPage.vue'),
    meta: { permission: 'phase1' }
  },
  {
    path: '/tools/formula',
    name: 'tool-formula',
    component: () => import('../pages/ToolFormulaPage.vue'),
    meta: { permission: 'tool_formula' }
  },
  {
    path: '/tools/auxpower',
    name: 'tool-auxpower',
    component: () => import('../pages/ToolAuxPowerPage.vue'),
    meta: { permission: 'tool_auxpower' }
  },
  {
    path: '/tools/engineering',
    name: 'tool-engineering',
    component: () => import('../pages/ToolEngineeringPage.vue'),
    meta: { permission: 'tool_engineering' }
  },
  {
    path: '/tools/datainject',
    name: 'tool-datainject',
    component: () => import('../pages/ToolDataInjectPage.vue'),
    meta: { permission: 'tool_datainject' }
  },
  {
    path: '/tools/conditions',
    name: 'tool-conditions',
    component: () => import('../pages/ToolConditionsPage.vue'),
    meta: { permission: 'tool_conditions' }
  },
  {
    path: '/tools/params',
    name: 'tool-params',
    component: () => import('../pages/ToolParamsPage.vue'),
    meta: { permission: 'tool_params' }
  },
  {
    path: '/tools/financial',
    name: 'tool-financial',
    component: () => import('../pages/ToolFinancialPage.vue'),
    meta: { permission: 'tool_financial' }
  },
  {
    path: '/tools/config',
    name: 'tool-config',
    component: () => import('../pages/ToolConfigPage.vue'),
    meta: { permission: 'tool_config' }
  },
  {
    path: '/tools/survey-view',
    name: 'tool-survey-view',
    component: () => import('../pages/ToolSurveyViewPage.vue'),
    meta: { permission: 'tool_survey_view' }
  },
  {
    path: '/tools/simulation-view',
    name: 'tool-simulation-view',
    component: () => import('../pages/ToolSimulationViewPage.vue'),
    meta: { permission: 'tool_simulation_view' }
  },
  {
    path: '/tools/report',
    name: 'tool-report',
    component: () => import('../pages/ToolReportPage.vue'),
    meta: { permission: 'tool_report' }
  },
  {
    path: '/tools/projects',
    name: 'tool-projects',
    component: () => import('../pages/ToolProjectsPage.vue'),
    meta: { permission: 'tool_projects' }
  },
  {
    path: '/tools/templates',
    name: 'tool-templates',
    component: () => import('../pages/ToolTemplatesPage.vue'),
    meta: { permission: 'tool_templates' }
  },
  {
    path: '/tools/rules',
    name: 'tool-rules',
    component: () => import('../pages/ToolRulesPage.vue'),
    meta: { permission: 'tool_rules' }
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import('../pages/AuthPage.vue')
  },
  {
    path: '/epc',
    name: 'epc',
    component: () => import('../pages/EpcPage.vue'),
    meta: { permission: 'epc' }
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('../pages/AdminPanelPage.vue'),
    meta: { permission: 'admin_panel' }
  },
  {
    path: '/orchestrator',
    name: 'orchestrator',
    component: () => import('../pages/OrchestratorPage.vue'),
    meta: { permission: 'orchestrator' }
  },
  {
    path: '/tools/quick-config',
    name: 'tool-quick-config',
    component: () => import('../pages/QuickConfigPage.vue'),
    meta: { permission: 'tool_quick_config' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/** 需要登录才能访问的路由 */
const protectedRoutes = [
  'phase1',
  'phase2',
  'phase3',
  'phase4',
  'phase5',
  'survey',
  'epc',
  'admin',
  'tool-quick-config'
]

router.beforeEach((to, from, next) => {
  // 检查是否需要登录
  if (protectedRoutes.includes(to.name)) {
    const token = sessionStorage.getItem('auth_token')
    if (!token) {
      next({ name: 'home' })
      return
    }

    // 检查权限
    if (to.meta?.permission) {
      try {
        const raw = sessionStorage.getItem('user_info')
        if (raw) {
          const user = JSON.parse(raw)
          const perms = user.permissions || {}
          const level = perms[to.meta.permission] || 'hidden'
          if (level === 'hidden') {
            // 无权访问，跳转首页
            next({ name: 'home' })
            return
          }
        }
      } catch {
        // 解析失败，放行让页面自行处理
      }
    }
  }
  next()
})

export default router
