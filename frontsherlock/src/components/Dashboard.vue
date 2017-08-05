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
        <span> Current Cycle: 1 </span> <br>
        <span> Cycle State: {{project.cycle_state}} </span> <br>
        <span> Cases Not Executed: {{project.NOT_EXECUTED}} </span> <br>
        <span> Cases Passed: {{project.PASSED}} </span> <br>
        <span> Cases Failed: {{project.ERROR}} </span> <br>
        <span> Cases Blocked: {{project.BLOCKED}} </span> <br>
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

</style>
