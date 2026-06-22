import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'
import SurveyPage from '../pages/SurveyPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: App,
  },
  {
    path: '/survey',
    name: 'survey',
    component: SurveyPage,
  },
  {
    path: '/survey/:id',
    name: 'survey-edit',
    component: SurveyPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router