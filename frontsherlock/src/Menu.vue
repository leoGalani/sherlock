<template>
  <div id="menu_Component">
    <nav class="uk-navbar-container" uk-navbar v-if="['login', 'register'].indexOf($route.name) === -1">
    <div class="uk-navbar-left">
      <ul class="uk-navbar-nav">
        <li>
          <router-link to="/"><img class="logo_menu" src='./assets/img/sherlock_name.png' style="width: 123px;"></router-link>
        </li>
      </ul>

    </div>
    <div class="uk-navbar-right">
      <ul class="uk-navbar-nav">
        <li v-if="['dashboard'].indexOf($route.name) > -1">
          <router-link to="/project/new" title="New Project" uk-tooltip="delay: 300" > <i class="material-icons" style="color: rgb(117, 117, 117);">note_add</i> </router-link>
        </li>
        <li v-else>
          <a><i class="material-icons" style="color: rgb(117, 117, 117);">build</i></a>
          <div class="uk-navbar-dropdown">
              <ul class="uk-nav uk-navbar-dropdown-nav" style="width:450px !important">
                  <router-link :to="{ path: '/project/view/'+projectId+'/scenario_cases' }">Manage Cases and Scenarios </router-link>
                  <hr style="width:150px">
                  <a href="#"><li>Edit project</li></a>
              </ul>
          </div>
        </li>

        <li v-else>
            <a href="#"><img src='./assets/img/projects.png'></a>
            <div class="uk-navbar-dropdown">
                <ul class="uk-nav uk-navbar-dropdown-nav">
                    <li class="uk-active">FAZER UM MODAL QUE MOSTRA PROJETOS RECENTES QUE O USUARIO FAZ PARTE - tem que fazer um endpoint para retornar esses valores</li>
                    <li>Projeto2</li>
                </ul>
            </div>
        </li>
        <li></li>
        <li class="nav_divider"></li>
        <li>
          <a href="#" title="Sherlock Settings" uk-tooltip="delay: 300">
            <i class="material-icons" style="color: rgb(117, 117, 117);">settings</i></a>
        </li>
        <li><a><i class="material-icons" style="color: rgb(117, 117, 117);">account_circle</i></a>
          <div class="uk-navbar-dropdown">
              <ul class="uk-nav uk-navbar-dropdown-nav" style="width:450px !important">
                  <router-link :to="{ path: '/project/view/'+projectId+'/scenario_cases' }"> My Settings </router-link>
                  <hr style="width:150px">
                  <a @Click="logoff()"> Logoff </a>
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
