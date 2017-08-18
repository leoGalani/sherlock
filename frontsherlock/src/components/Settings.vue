<template>
  <div class="settings">
    <h2> Sherlock Settings </h2>
    <div class="content uk-width-medium-2-4 uk-container-center">
      <form v-on:submit="editSettings" class="uk-form-horizontal uk-margin-large">

        <div class="uk-grid" v-for="setting in settings">
          <div class="uk-margin">
              <div class="uk-form-label">{{setting.label}}</div>
              <div class="uk-form-controls uk-form-controls-text">
                  <label><input class="uk-radio" type="radio" :name="setting.setting"
                     value="True" v-model="setting.value" :checked="true"> Yes </label><br>
                  <label><input class="uk-radio" type="radio" :name="setting.setting"
                     value="False" v-model="setting.value"> No </label><br>
              </div>
          </div>
        </div>

        <button class="uk-button uk-button-default">Save Settings</button>
      </form>
    </div>
  </div>
</template>

<script>
import UIkit from 'uikit'
export default {
  name: 'settings',
  data () {
    return {
      settings: [],
      currentUser: ''
    }
  },
  methods: {
    getSherlockSettings () {
      this.$http.get('dashboard/get_settings').then(function (response) {
        this.settings = response.body
      })
    },
    editSettings (e) {
      e.preventDefault()
      this.$http.post('dashboard/set_settings', this.settings).then(function (response) {
        UIkit.notification('<span uk-icon="icon: check"></span> Settings Save!', {status: 'success', timeout: '700'})
      })
    }
  },
  created: function () {
    this.getSherlockSettings()
    this.currentUser = JSON.parse(window.localStorage.getItem('user'))
    if (this.currentUser.profile !== 'admin') {
      this.$router.push({name: 'dashboard'})
    }
  }
}
</script>

<style scoped>

.settings{
  padding: 15px;
}

</style>
