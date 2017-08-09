<template>
  <div class="dashboard">
    <h2> Edit Project </h2>
    <div class="content uk-width-medium-2-4 uk-container-center">
      <form v-on:submit="editProject" class="uk-form-horizontal uk-margin-large">
        <p>Projects in sherlock are like containers for your test cenarios and cases.</p>
        <div class="uk-margin">
            <label class="uk-form-label" for="form-horizontal-text">Project Name</label>
            <div class="uk-form-controls uk-form-width-large">
                <input class="uk-input" id="form-horizontal-text" type="text" v-model="project_name" >
            </div>
        </div>

        <div class="uk-margin">
          <div class="uk-form-label">Project Owner</div>
          <div class="uk-form-controls">
            <select  v-model="project_owner_id" class="uk-select">
              <option v-for="user in users" :value="user.id"
              :selected="user.id == project_owner_id">
              {{ user.email }} </option>
            </select>
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
                   value="WEB" v-model="type_of_project" :checked="true"> Web </label><br>
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
      projectId: '',
      project_name: '',
      privacy_policy: '',
      type_of_project: '',
      project_owner: '',
      project_owner_id: '',
      users: []
    }
  },
  methods: {
    editProject () {
      if (!this.project_name || !this.type_of_project || !this.privacy_policy) {
        UIkit.notification('Please fill all the inputs', {status: 'danger', timeout: 700})
      } else {
        let editedProject = {
          project_name: this.project_name,
          type_of_project: this.type_of_project,
          privacy_policy: this.privacy_policy,
          project_owner: this.project_owner_id
        }
        this.$http.post('project/edit/' + this.projectId, editedProject).then(function (response) {
          UIkit.notification('<span uk-icon="icon: check"></span> Project edited with Success', {status: 'success', timeout: '700'})
          this.$router.push({name: 'dashboard'})
        })
      }
    },
    get_all_users () {
      this.$http.get('user/get_all_users').then(function (response) {
        this.users = response.body
      })
    },
    get_project_details () {
      this.$http.get('project/show/' + this.projectId).then(function (response) {
        this.project_name = response.body.name
        this.privacy_policy = response.body.privacy_policy
        this.type_of_project = response.body.type_of_project
        this.project_owner_name = response.body.owner_name
        this.project_owner_id = response.body.owner_id
      })
    }
  },
  created: function () {
    this.get_all_users()
    this.projectId = this.$route.params.projectId
    this.get_project_details()
  },
  mounted: function () {
  }
}
</script>

<style scoped>

.dashboard{
  padding: 15px;
}

</style>
