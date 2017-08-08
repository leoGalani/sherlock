// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import VueResource from 'vue-resource'
import App from './App'
import router from './router'
import UIkit from 'uikit'

require('./assets/main.css')
Vue.config.productionTip = false
Vue.use(VueResource)
Vue.http.options.root = '/api'
Vue.http.options.crossOrigin = true

Vue.http.interceptors.push(function (request, next) {
  const tokenData = JSON.parse(window.localStorage.getItem('auth'))
  if (tokenData) {
    request.headers.set('accept', 'application/json')
    request.headers.set('authorization', 'Basic ' + btoa(tokenData.token + ':'))
  }

  next(function (response) {
    if (response.status === 401) {
      UIkit.notification('Please Login', {status: 'warning', timeout: '700'})
      window.localStorage.removeItem('user')
      window.localStorage.removeItem('auth')
      this.$router.push({path: '/login'})
    }
    if (response.status === 400) {
      UIkit.notification('Something went wrong', {status: 'danger', timeout: '700'})
    }

    if (response.status === 404) {
      UIkit.notification('The item you looking for no longer exist', {status: 'warning', timeout: '700'})
      this.$router.push({path: '/dashboard'})
    }
  })
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
