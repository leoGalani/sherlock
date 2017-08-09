<template>
  <div id="base_app">
    <app-menu></app-menu>
    <router-view></router-view>
    <app-footer></app-footer>
  </div>
</template>

<script>
import Menu from '@/Menu.vue'
import Footer from '@/Footer.vue'

export default {
  name: 'base_app',
  data () {
    return {
    }
  },
  created: function () {

  },
  updated: function () {

  },
  components: {
    AppMenu: Menu,
    AppFooter: Footer
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
