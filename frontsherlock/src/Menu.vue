<template>
  <div id="menu_Component">
    <nav class="uk-navbar-container" uk-navbar v-if="['login', '404', 'register'].indexOf($route.name) === -1">
    <div class="uk-navbar-left">
      <ul class="uk-navbar-nav">
        <li>
          <router-link :to="{name: 'dashboard'}"><img class="logo_menu" src='./assets/img/sherlock_name.png' style="width: 123px;"></router-link>
        </li>
      </ul>

    </div>
    <div class="uk-navbar-right">
      <ul class="uk-navbar-nav">
        <li v-if="['dashboard', 'new_project'].indexOf($route.name) > -1">
          <router-link to="/project/new" title="New Project" uk-tooltip="delay: 300" > <i class="material-icons" style="color: rgb(117, 117, 117);">note_add</i> </router-link>
        </li>
        <li v-else>
          <a><i class="material-icons" style="color: rgb(117, 117, 117);">build</i></a>
          <div uk-dropdown="delay-hide: 50;">
            <ul class="uk-nav uk-dropdown-nav">
                <router-link :to="{ path: '/project/view/'+projectId+'/scenario_cases' }">Manage Cases and Scenarios </router-link>
                <hr style="width:150px">
                <router-link :to="{ path: '/project/edit/'+projectId }">Edit Project </router-link>
            </ul>
          </div>
        </li>
        <li class="nav_divider"></li>
        <li>
          <router-link title="Sherlock Settings" uk-tooltip="delay: 300"
          :to="{ path: 'settings' }">
            <i class="material-icons" style="color: rgb(117, 117, 117);">settings</i>
          </router-link>
        </li>
        <li>
          <a><i class="material-icons" style="color: rgb(117, 117, 117);">account_circle</i></a>
          <div uk-dropdown="delay-hide: 50;">
            <ul class="uk-nav uk-dropdown-nav">
              <li><router-link :to="{ path: '/project/view/'+projectId+'/scenario_cases' }"> My Settings </router-link></li>
              <li><hr style="width:150px"></li>
            <li><a @click="logoff()"> Logoff </a></li>
            <li><a href="http://sherlockqa.readthedocs.io/" target="_blank" uk-icon="icon: question"> Help </a></li>
            </ul>
          </div>
        </li>

      </ul>
    </div>
  </nav>
  </div>
</template>

<script>
import UIkit from 'uikit'

export default {
  name: 'menu_Component',
  data () {
    return {
      projectId: ''
    }
  },
  methods: {
    logoff () {
      UIkit.notification('See you later!')
      window.localStorage.removeItem('user')
      window.localStorage.removeItem('auth')
      this.$router.push({path: '/login'})
    }
  },
  updated: function () {
    if (['login', 'register', 'dashboard'].indexOf(this.$route.name) === -1) {
      // this.$route.params.projectId
      this.projectId = this.$route.params.projectId
    }
  }
}
</script>

<style scoped>

.nav_divider{
    background-color: rgb(117, 117, 117);
    width: 1px;
    height: 30px;
    margin-top: 21px;
}

</style>
