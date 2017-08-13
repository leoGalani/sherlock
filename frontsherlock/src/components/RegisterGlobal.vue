<template>
  <div class="register">
    <div uk-grid class="uk-container-center">
      <div class="uk-width-1-3"> </div>
      <div class="uk-width-1-3" style="margin-top: 5%;">
          <center><img src='../assets/img/sherlock.png' style="width:80%;">
            <form v-on:submit.prevent="handleRegister()">
            <div>
              <p> Please, fill all the form inputs. </p>
              <div class="uk-margin">
                  <div class="uk-form-controls uk-width-2-3@s">
                    <div class="uk-inline">
                        <span class="uk-form-icon" uk-icon="icon: user"></span>
                        <input class="uk-input" id="form-horizontal-text" placeholder="Name" type="text" v-model="register.name">
                      </div>
                  </div>
              </div>

              <div class="uk-margin">
                  <div class="uk-form-controls uk-width-2-3@s">
                    <div class="uk-inline">
                        <span class="uk-form-icon" uk-icon="icon: user"></span>
                        <input class="uk-input" id="form-horizontal-text" placeholder="Email" type="text" v-model="register.email">
                      </div>
                  </div>
              </div>
              <div class="uk-margin">
                  <div class="uk-form-controls uk-width-2-3@s">
                    <div class="uk-inline">
                        <span class="uk-form-icon" uk-icon="icon: lock"></span>
                        <input class="uk-input" id="form-horizontal-text" placeholder="Password" type="password" v-model="register.password">
                    </div>
                  </div>
              </div>

              <div class="uk-margin">
                  <div class="uk-form-controls uk-width-2-3@s">
                    <div class="uk-inline">
                        <span class="uk-form-icon" uk-icon="icon: copy"></span>
                        <input class="uk-input" id="form-horizontal-text" placeholder="Confirm Password" v-model="register.confirmPassword" type="password">
                    </div>
                  </div>
              </div>

              <button class="uk-button uk-button-default" type="Submit" style="margin-right:15px; ">Register</button>
              <router-link class="uk-button uk-button-default" :to="{ name: 'login' }">Cancel</router-link>
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
  name: 'register',
  data () {
    return {
      register: {
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    handleRegister () {
      console.log(this.register.name)
      if (!this.register.name || !this.register.email || !this.register.password) {
        UIkit.notification('<span uk-icon="icon: ban"></span> Fields cannot be empty', {timeout: '700'})
        return
      }
      var newUser = {
        'name': this.register.name,
        'email': this.register.email,
        'password': this.register.password
      }
      this.$http.post('user/new', newUser).then(function (response) {
        if (response.body.message === 'UNAUTHORIZED') {
          UIkit.notification('<span uk-icon="icon: ban"></span> This Function is no available.', {timeout: '700'})
          this.$router.push({path: '/'})
        } else if (response.body.message === 'EMAIL_IN_USE') {
          UIkit.notification('<span uk-icon="icon: ban"></span> This email is already in use.', {timeout: '700'})
          return
        } else {
          UIkit.notification('<span uk-icon="icon: check"></span> User created.', {timeout: '700'})
          this.$router.push({path: '/'})
        }
      })
    },
    checkGlobalRegister () {
      this.$http.get('dashboard/check_global_register_permission').then(function (response) {
        if (response.body.permission === false) {
          UIkit.notification('This Function is no available.', {timeout: '700'})
          this.$router.push({path: '/'})
        }
      })
    }
  },
  created: function () {
    this.checkGlobalRegister()
  }
}
</script>

<style scoped>
.uk-inline{
  width: 100%;
}
</style>
