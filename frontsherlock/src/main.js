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
Vue.http.options.root = 'http://localhost:5000'
Vue.http.options.crossOrigin = true

Vue.http.interceptors.push(function (request, next) {
  const tokenData = JSON.parse(window.localStorage.getItem('auth'))
  if (tokenData) {
    request.headers.set('accept', 'application/json')
    request.headers.set('authorization', 'Basic ' + btoa(tokenData.token + ':'))
  }

  next(function (response) {
    if (response.status === 401) {
      UIkit.notification('Please Login Again.', {status: 'warning'})
      window.localStorage.removeItem('user')
      window.localStorage.removeItem('auth')
      this.$router.push({path: '/login'})
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
