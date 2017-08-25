<template>
  <div class="dashboard">
    <div  id="loading" v-if="loading">
       <center><div uk-spinner></div>
       Loading...</center>
     </div>
    <h2 v-if="showTitle"> Current Projects </h2>

    <div v-for="project in projects.projects" class="project_box">
      <router-link :to="{ path: 'project/view/'+project.id }" class="box-link">
        <h4 class="hide_overflow">{{project.name}}</h4>
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

    <div v-if="showGreetings">
      <hr>
      <center><h2 style="margin-left:20px"><span class="uk-margin-small-right" uk-icon="icon: heart"></span> Hey, this seems like a brand new installation!  Thanks for giving sherlock a try! <span class="uk-margin-small-right" uk-icon="icon: heart"></span></h2>
        <h3> Hmm seems like you don't have any project yet... </h3>
        <img src='../assets/img/sherlock_raposa_bored.png'>
        <h3>
            You can start creating your first one here: <router-link :to="{ name: 'new_project' }" title="New Project" uk-tooltip="delay: 300" > <i class="material-icons" style="color: rgb(117, 117, 117);">note_add</i> </router-link>
        </h3>

        <h3> Also checkout a demo on how to use Sherlock </h3>
        <iframe width="560" height="315" src="https://www.youtube.com/embed/bAMoUoXXLUU" frameborder="0" allowfullscreen></iframe>


      </center>


    </div>

  </div>
</template>

<script>
export default {
  name: 'dashboard',
  data () {
    return {
      projects: [],
      loading: false,
      showTitle: false,
      showGreetings: false
    }
  },
  methods: {
    fetchProjects: function () {
      this.$http.get('dashboard/').then(response => {
        this.loading = false
        this.projects = response.body
        if (this.projects.projects.length > 0) {
          this.showTitle = true
          this.showGreetings = false
        } else {
          this.showGreetings = true
          this.showTitle = false
        }
      })
    }
  },
  created: function () {
    this.loading = true
    this.fetchProjects()
    this.interval = setInterval(function () {
      this.fetchProjects()
    }.bind(this), 2000)
  },
  updated: function () {
    //  this.fetchProjects()
  },
  beforeDestroy: function () {
    clearInterval(this.interval)
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
