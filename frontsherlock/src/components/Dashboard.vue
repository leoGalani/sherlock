<template>
  <div class="dashboard">
    <div  id="loading" v-if="loading">
       <center><div uk-spinner></div>
       Loading...</center>
     </div>
    <h2> Current Projects </h2>

    <div v-for="project in projects.projects" class="project_box">
      <router-link :to="{ path: 'project/view/'+project.id }" class="box-link">
        <h4>{{project.name}}</h4>
        <hr>
        <span v-if="project.have_cycle === true">
          <span> Current Cycle:  {{project.current_cycle}} </span> <br>
          <span> Cycle State: {{project.cycle_state}} </span> <br>
          <span> Cases Not Executed: {{project.stats.total_not_executed}} </span> <br>
          <span> Cases Passed: {{project.stats.total_passed}} </span> <br>
          <span> Cases Failed: {{project.stats.total_error}} </span> <br>
          <span> Cases Blocked: {{project.stats.total_blocked}} </span> <br>
        </span>
        <span v-else>
          <center><i class="material-icons">cake</i>
          <p>Brand new project! <br> no cyles yet!</p></center><br>
        </span>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'dashboard',
  data () {
    return {
      projects: [],
      loading: false
    }
  },
  methods: {
    fetchProjects: function () {
      this.loading = true
      this.$http.get('dashboard/').then(response => {
        this.loading = false
        this.projects = response.body
      })
    }
  },
  created: function () {
    this.fetchProjects()
  },
  updated: function () {
    //  this.fetchProjects()
  }
}
</script>

<style scoped>

.dashboard div{
  padding: 10px;
}

.project_box{
  min-height: 210px;
}

</style>
