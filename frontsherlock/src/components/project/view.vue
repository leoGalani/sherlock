<template>
  <div class="project details">
    <div class="uk-grid">
      <div class="uk-width-3-4">
        <h2> Project [{{project.name}}] Dashboard </h2>
          <div class="content"> </div>
      </div>
      <div class="uk-width-1-4 uk-text-center">
        <h2> Project Details </h2>
        <div class="content">
          <span><i class="material-icons project_avatar">language</i></span><br>
          <span> Type of Project: <b>{{project.type_of_project}}</b></span><br>
          <span> Privacy Policy:<b> {{project.privacy_policy}}</b> </span><br>
          <span> Owner: <b>{{project.owner_name}}</b></span><br>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UIkit from 'uikit'

export default {
  name: 'projectdetails',
  data () {
    return {
      project: ''
    }
  },
  methods: {
    fetchProject (projectId) {
      this.$http.get('project/show/' + projectId)
      .then(function (response) {
        this.project = response.body
        this.project.type_of_project = this.project.type_of_project.toLowerCase()
        this.project.privacy_policy = this.project.privacy_policy.toLowerCase()
      }, function (response) {
        if (response.body.message === 'PROJECT_NOT_FOUND') {
          UIkit.notification('Project Not Found.', {status: 'danger'})
          this.$router.push({path: '/'})
        }
      })
    }
  },
  created: function () {
    this.fetchProject(this.$route.params.projectId)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.project_avatar{
  font-size: 150px;
}
.content{
  width: 80%;
  margin-left: 10px;
}
</style>
