<template>
  <div class="login">
    <div uk-grid class="uk-container-center">
      <div class="uk-width-1-3"> </div>
      <div class="uk-width-1-3" style="margin-top: 5%;">
          <center><img src='../assets/img/sherlock.png' style="width:80%;">
            <form v-on:submit.prevent="handleLogin()">
            <div>
              <div class="uk-margin">
                  <div class="uk-form-controls uk-width-2-3@s">
                    <div class="uk-inline">
                        <span class="uk-form-icon" uk-icon="icon: user"></span>
                        <input class="uk-input" id="form-horizontal-text" placeholder="Email" type="text" v-model="login.email">
                      </div>
                  </div>
              </div>
              <div class="uk-margin">
                  <div class="uk-form-controls uk-width-2-3@s">
                    <div class="uk-inline">
                        <span class="uk-form-icon" uk-icon="icon: lock"></span>
                        <input class="uk-input" id="form-horizontal-text" placeholder="Password" type="password" v-model="login.password">
                    </div>
                  </div>
              </div>

              <button class="uk-button uk-button-default" type="Submit" style="margin-right:15px; ">Login</button>
              <router-link v-if="show_register_button" class="uk-button uk-button-default" :to="{ name: 'registerg' }">Register</router-link>
            </div>
            </form>
          </center>
        </div>
        <div class="uk-width-1-3"></div>
      </div>
  </div>
</template>

<script>
import UIkit from 'uikit'

export default {
  name: 'login',
  data () {
    return {
      login: {
        email: '',
        password: ''
      },
      show_register_button: false
    }
  },
  methods: {
    checkOpenRegister () {
      this.$http.get('dashboard/check_global_register_permission').then(function (response) {
        if (response.body.permission === false) {
          this.show_register_button = false
        } else {
          this.show_register_button = true
        }
      })
    },
    handleLogin () {
      if (!this.login.email || !this.login.password) {
        UIkit.notification('Please fill all the inputs', {status: 'danger'})
        return
      }
      var getAuthToken = {
        url: 'auth_token',
        method: 'POST',
        headers: { Authorization: 'Basic ' + btoa(this.login.email + ':' + this.login.password) }
      }

      const auth = {}
      const user = {}
      this.$http(getAuthToken).then((response) => {
        auth.token = response.body.token
        window.localStorage.setItem('auth', JSON.stringify(auth))

        this.$http.get('user/get_user_email/' + this.login.email).then(response => {
          user.email = response.body.email
          user.user_id = response.body.id
          user.name = response.body.name
          user.profile = response.body.profile
          window.localStorage.setItem('user', JSON.stringify(user))
          this.$router.push({path: '/dashboard'})
        }, (response) => {
          UIkit.notification('<span uk-icon="icon: ban"></span> User ' + this.email + 'might be corrupted', {status: 'danger', timeout: '700'})
        })
      }, (response) => {
        UIkit.notification('<span uk-icon="icon: ban"></span> Wrong Email or Password', {status: 'danger', timeout: '700'})
      })
    }
  },
  created: function () {
    window.localStorage.removeItem('user')
    window.localStorage.removeItem('auth')
    this.interval = setInterval(function () {
      this.checkOpenRegister()
    }.bind(this), 7000)
  },
  mounted: function () {
    this.checkOpenRegister()
  },
  beforeDestroy: function () {
    clearInterval(this.interval)
  }
}
</script>

<style scoped>
.uk-inline{
  width: 100%;
}
</style>
