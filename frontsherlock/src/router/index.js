import Vue from 'vue'
import Router from 'vue-router'

import Login from '@/components/Login'
import Dashboard from '@/components/Dashboard'
import AddProject from '@/components/project/Add'
import ProjectDetails from '@/components/project/View'
import ScenarioCases from '@/components/scenario_cases/Dashscenarios'
import ProjectCycles from '@/components/cycles/Dashcycles'
// import UIkit from 'uikit'

Vue.use(Router)

const router = new Router({
  routes: [
    {path: '/', name: 'login_root', component: Login},
    {path: '/login', name: 'login', component: Login},
    {path: '/dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true }},
    {path: '/project/new', name: 'new_project', component: AddProject, meta: { requiresAuth: true }},
    {path: '/project/view/:projectId', name: 'view_project', component: ProjectDetails, meta: { requiresAuth: true }},
    {path: '/project/view/:projectId/scenario_cases/', name: 'scenario_cases', component: ScenarioCases, meta: { requiresAuth: true }},
    {path: '/project/view/:projectId/cycle/:cycleId', name: 'project_cycles', component: ProjectCycles, meta: { requiresAuth: true }}
  ]
})

export default router

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const auth = JSON.parse(window.localStorage.getItem('auth'))
    const user = JSON.parse(window.localStorage.getItem('user'))
    if (!auth || !user) {
      router.push({path: '/login'})
    }
  }
  next()
})
