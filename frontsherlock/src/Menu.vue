<template>
  <div id="menu_Component">
    <nav class="uk-navbar-container" uk-navbar v-if="['login', '404', 'registerg', 'register'].indexOf($route.name) === -1">
    <div class="uk-navbar-left">
      <ul class="uk-navbar-nav">
        <li>
          <router-link :to="{name: 'dashboard'}"><img class="logo_menu" src='./assets/img/sherlock_name.png' style="width: 123px;"></router-link>
        </li>
      </ul>

    </div>
    <div class="uk-navbar-right">
      <ul class="uk-navbar-nav">
        <li v-if="['dashboard', 'new_project', 'settings', 'user_edit'].indexOf($route.name) > -1">
          <router-link :to="{ name: 'new_project' }" title="New Project" uk-tooltip="delay: 300" > <i class="material-icons" style="color: rgb(117, 117, 117);">note_add</i> </router-link>
        </li>
        <li v-else>
          <a>
            <span class="project_settings">
              <span>
                <i class="material-icons" style="color: rgb(248, 248, 248); margin-top:5px">build</i>
              </span>
              <span style="padding: 6px; color: rgb(248, 248, 248);">
                {{project.name}} Settings
              </span>
            </span>
          </a>
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
          <router-link v-if="this.currentUser.profile === 'admin'"
          title="Sherlock Settings" uk-tooltip="delay: 300"
          :to="{ name: 'settings' }">
            <i class="material-icons" style="color: rgb(117, 117, 117);">settings</i>
          </router-link>
        </li>
        <li>
          <a><i class="material-icons" style="color: rgb(117, 117, 117);">account_circle</i></a>
          <div uk-dropdown="delay-hide: 50;">
            <ul class="uk-nav uk-dropdown-nav">
              <li><router-link :to="{ name: 'user_edit' }"> My Settings </router-link></li>
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
      projectId: '',
      currentUser: '',
      project: ''
    }
  },
  methods: {
    logoff () {
      UIkit.notification('See you later!', {timout: '700'})
      window.localStorage.removeItem('user')
      window.localStorage.removeItem('auth')
      this.$router.push({path: '/login'})
    },
    getUserInfo () {
      this.currentUser = JSON.parse(window.localStorage.getItem('user'))
    },
    getProjectInfo () {
      this.$http.get('project/show/' + this.$route.params.projectId).then(function (response) {
        this.project = response.body
      },
      function (response) {
      })
    }
  },
  updated: function () {
    if (['login', 'register', 'dashboard'].indexOf(this.$route.name) === -1) {
      this.projectId = this.$route.params.projectId
    }
  },
  watch: {
    $route: function () {
      if (['login', 'register'].indexOf(this.$route.name) === -1) {
        this.getUserInfo()
        if (['dashboard', 'new_project', 'settings', 'user_edit'].indexOf(this.$route.name) === -1) {
          this.getProjectInfo()
        }
      }
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

.project_settings{
  border-radius: 7px;
  height: 33px;
  background-color: #666666;
  display: inline-flex;
  padding: 3px;
  text-transform: none;
  font-weight: 300;

}

</style>
