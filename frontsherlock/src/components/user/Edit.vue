<template>
  <div class="edituser">
    <h2> Edit User </h2>
    <div class="content uk-width-medium-2-4 uk-container-center">
      <form v-on:submit="editUser" class="uk-form-horizontal uk-margin-large">
        <div class="uk-margin">
            <label class="uk-form-label" for="form-horizontal-text">Your Name</label>
            <div class="uk-form-controls uk-form-width-large">
                <input class="uk-input" id="form-horizontal-text" type="text" v-model="name">
            </div>
        </div>

        <div class="uk-margin">
            <label class="uk-form-label" for="form-horizontal-text">Your Email</label>
            <div class="uk-form-controls uk-form-width-large">
                <input class="uk-input" id="form-horizontal-text" type="text" v-model="email">
            </div>
        </div>

        <div class="uk-margin">
            <label class="uk-form-label" for="form-horizontal-text">Your Password <span v-if="this.confirmPassword.length > 1 && this.password === this.confirmPassword" uk-icon="icon: check"></span></label>
            <div class="uk-form-controls uk-form-width-large">
                <input class="uk-input" id="form-horizontal-text" placeholder="leave it blank if you dont want to edit it"type="password" v-model="password">
            </div>
        </div>

        <div class="uk-margin" v-if="password.length > 1">
            <label class="uk-form-label" for="form-horizontal-text">Confirm Password <span v-if="this.password ===this.confirmPassword" uk-icon="icon: check"></span></label>
            <div class="uk-form-controls uk-form-width-large">
                <input class="uk-input" id="form-horizontal-text" placeholder="Type your new password again" type="password" v-model="confirmPassword">
            </div>
        </div>

        <button class="uk-button uk-button-default">Save Info</button>
      </form>
    </div>
  </div>
</template>

<script>
import UIkit from 'uikit'

export default {
  name: 'edituser',
  data () {
    return {
      currentUser: '',
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    editUser (e) {
      e.preventDefault()
      if (!this.name || !this.email) {
        UIkit.notification('<span uk-icon="icon: ban"></span>You can`t save blank data', {status: 'danger', timeout: 700})
      } else {
        let editedUser = {
          name: this.name,
          email: this.email
        }

        if (this.password) {
          if (!this.confirmPassword) {
            UIkit.notification('<span uk-icon="icon: ban"></span> You need to confirm your new password', {status: 'danger', timeout: 700})
            return
          }
          if (this.password !== this.confirmPassword) {
            UIkit.notification('<span uk-icon="icon: ban"></span> The passwords dont match!', {status: 'danger', timeout: 700})
            return
          }
          editedUser.password = this.password
        }
        this.$http.post('user/edit/' + this.currentUser.user_id, editedUser).then(function (response) {
          UIkit.notification('<span uk-icon="icon: check"></span> Info saved!', {status: 'success', timeout: '700'})
          let user = {
            name: editedUser.name,
            email: editedUser.email,
            user_id: this.currentUser.user_id,
            profile: this.currentUser.profile
          }
          window.localStorage.removeItem('user')
          window.localStorage.setItem('user', JSON.stringify(user))
        })
      }
    },
    getUserDetails () {
      this.$http.get('user/get_user_id/' + this.currentUser.user_id).then(function (response) {
        this.name = response.body.name
        this.email = response.body.email
      })
    }
  },
  created: function () {
    this.currentUser = JSON.parse(window.localStorage.getItem('user'))
    this.getUserDetails()
  },
  mounted: function () {
  }
}
</script>

<style scoped>

.edituser{
  padding: 15px;
}

</style>
