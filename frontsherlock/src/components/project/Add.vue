<template>
  <div class="dashboard">
    <h2> Add Project </h2>
    <div class="content uk-width-medium-2-4 uk-container-center">
      <form v-on:submit="addProject" class="uk-form-horizontal uk-margin-large">
        <p>Projects in sherlock are like containers for your test cenarios and cases.</p>
        <div class="uk-margin">
            <label class="uk-form-label" for="form-horizontal-text">Project Name</label>
            <div class="uk-form-controls uk-form-width-large">
                <input class="uk-input" id="form-horizontal-text" type="text" v-model="project_name" >
            </div>
        </div>

        <div class="uk-margin">
            <div class="uk-form-label">Privacy</div>
            <div class="uk-form-controls uk-form-controls-text">
                <label><input class="uk-radio" type="radio"
                   value="PUBLIC" v-model="privacy_policy"> Public </label><br>
                <label><input class="uk-radio" type="radio"
                   value="PRIVATE" v-model="privacy_policy"> Private </label>
            </div>
        </div>

        <div class="uk-margin">
            <div class="uk-form-label">Type of Project</div>
            <div class="uk-form-controls uk-form-controls-text">
                <label><input class="uk-radio" type="radio" name="type_of_project"
                   value="WEB" v-model="type_of_project"> Web </label><br>
                <label><input class="uk-radio" type="radio" name="type_of_project"
                   value="MOBILE" v-model="type_of_project"> Mobile </label><br>
                <label><input class="uk-radio" type="radio" name="type_of_project"
                   value="API" v-model="type_of_project"> API </label>
            </div>
        </div>

        <button class="uk-button uk-button-default">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import UIkit from 'uikit'

export default {
  name: 'dashboard',
  data () {
    return {
      project_name: '',
      privacy_policy: 'PUBLIC',
      type_of_project: 'WEB'
    }
  },
  methods: {
    addProject (e) {
      if (!this.project_name || !this.type_of_project || !this.privacy_policy) {
        UIkit.notification('<span uk-icon="icon: ban"></span> Please fill all the inputs', {status: 'danger'})
      } else {
        var user = JSON.parse(window.localStorage.getItem('user'))
        let newProject = {
          project_name: this.project_name,
          type_of_project: this.type_of_project,
          privacy_policy: this.privacy_policy,
          project_owner: user.user_id
        }
        e.preventDefault()
        this.$http.post('project/new', newProject)
        .then(function (response) {
          UIkit.notification('<span uk-icon="icon: check"></span> Project added with Success', {status: 'success', timeout: '700'})
          this.$router.push({name: 'dashboard'})
        })
        e.preventDefault()
      }
    }
  }
}
</script>

<style scoped>

.dashboard{
  padding: 15px;
}

</style>
