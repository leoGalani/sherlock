<template>
  <div id="base_app">
    <app-menu></app-menu>
    <router-view></router-view>
  </div>
</template>

<script>
import Menu from '@/Menu.vue'

export default {
  name: 'base_app',
  data () {
    return {
      alert_msg: ''
    }
  },
  created: function () {

  },
  updated: function () {

  },
  components: {
    AppMenu: Menu
  }
}
</script>

<style scoped>

.nav_divider{
    background-color: orange;
    width: 1px;
    height: 30px;
    margin-top: 21px;
}
</style>
