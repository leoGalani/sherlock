<template>
  <div class="project details">
    <div class="uk-grid">
      <div class="uk-width-3-4">
        <h2><span class="title_span"> {{project.name}} - Project Dashboard </span></h2>
        <div class="content" style="width: 100%; min-height: 400px;">
          <div class="uk-child-width-1-2@s uk-grid-match" uk-grid>
            <router-link v-if="project.have_scenarios === false" :to="{ path: '/project/view/'+projectId+'/scenario_cases' }">
            <div>
              <div class="uk-card uk-card-small uk-card-default uk-card-hover uk-card-body">
                <h4 class="uk-card-title">This project have no scenarios!</h4>
                <p>Click here to create cenarios and test cases for this project.</p>
              </div>
            </div>
          </router-link>

          <div v-if="project.have_cycles === false && project.have_scenarios === false">
            <div class="uk-card uk-card-small uk-card-default uk-card-body">
              <h4 class="uk-card-title">This project have no cycles!</h4>
              <p>You can't have cycles without test cases!</p>
            </div>
          </div>
            <div v-if="project.have_cycles === false && project.have_scenarios" @click="createCycle()" style="cursor:pointer;">
              <div class="uk-card uk-card-small uk-card-default uk-card-hover uk-card-body">
                <h4 class="uk-card-title">This project have no cycles!</h4>
                <p>Click here to create cenarios and test cases for this project.</p>
              </div>
            </div>
          </div>
          <div class="uk-grid" v-if="project.have_cycles">
            <div class="uk-width-3-5">
              <h3>Current cycle stats</h3>
              <div class="ct-chart">
                <div v-if="display_load_chart">
                  <div uk-spinner></div>
                  Loading chart
                </div>
              </div>
            </div>
            <div class="uk-width-2-5">
              <h3>Cycle {{this.current_cycle.cycle}} status </h3>
              <div> <b>created at: </b> {{this.current_cycle.created_at}} <a title="dd-mm-yyyy" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: question"></a></div>
              <div> <b>cases not executed: </b> {{this.current_cycle.stats.total_not_executed}} </div>
              <div> <b>cases passed: </b> {{this.current_cycle.stats.total_passed}} </div>
              <div> <b>cases failed: </b> {{this.current_cycle.stats.total_error}} </div>
              <div> <b>cases blocked: </b> {{this.current_cycle.stats.total_blocked}} </div>
              <router-link class="uk-button uk-button-default" style='margin-top:10px;' :to="{ name: 'project_cycles', params: {projectId: this.projectId, cycleId: this.current_cycle.id} }">Execute Test Cases</router-link>
            </div>
          </div>
          <hr>
        </div>
      </div>
      <div class="uk-width-1-4">
        <h2><span class="title_span"> Project Details </span>  </h2>
        <div class="content">
          <center><span><i class="material-icons project_avatar">language</i></span></center><br>
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
import Chartist from 'chartist'

export default {
  name: 'projectdetails',
  data () {
    return {
      project: '',
      projectId: '',
      current_cycle: {
        'stats': {
          'total_not_executed': '',
          'total_not_passed': '',
          'total_not_blocked': '',
          'total_not_error': ''
        }
      },
      display_load_chart: true
    }
  },
  methods: {
    fetchProject () {
      this.$http.get('project/show/' + this.projectId).then(function (response) {
        this.project = response.body
        this.project.type_of_project = this.project.type_of_project.toLowerCase()
        this.project.privacy_policy = this.project.privacy_policy.toLowerCase()
        this.current_cycle = this.project.last_cycle
      },
      function (response) {
        if (response.body.message === 'PROJECT_NOT_FOUND') {
          UIkit.notification('Project Not Found.', {status: 'danger'})
          this.$router.push({path: '/'})
        }
      })
    },
    createCycle () {
      if (this.project.have_scenarios) {
        var vueInstance = this
        UIkit.modal.prompt('Want to give this cycle a name?* (not required):', '').then(function (cycleName) {
          if (cycleName === null) {
            return
          }
          vueInstance.$http.post('projects/' + vueInstance.projectId + '/cycle/new', {'cycle_name': cycleName})
          .then(function (response) {
            if (response.body.message === 'CYCLE_CREATED') {
              UIkit.notification('<span uk-icon="icon: check"></span> Cycle Created', {timeout: '700'})
              this.$router.push({name: 'project_cycles', params: { projectId: vueInstance.projectId, cycleId: response.body.cycle_id }})
            } else {
              UIkit.notification('<span uk-icon="icon: ban"></span> Please close the current cycle', {timeout: '700'})
            }
          })
        }, function () {
          return
        })
      }
    },
    mount_chart () {
      if (this.project.have_cycles) {
        var citem = this.current_cycle.stats
        Chartist.Bar('.ct-chart', {
          labels: ['passed', 'failed', 'blocked', 'not executed'],
          series: [citem.total_passed, citem.total_error, citem.total_blocked, citem.total_not_executed]
        }, {
          distributeSeries: true
        })
        this.display_load_chart = false
      }
    }
  },
  created: function () {
    this.projectId = this.$route.params.projectId
    this.fetchProject(this.$route.params.projectId)
  },
  mounted: function () {
    this.mount_chart()
    this.interval = setInterval(function () {
      this.mount_chart()
    }.bind(this), 1000)
  },
  beforeDestroy: function () {
    clearInterval(this.interval)
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

.uk-card-default .uk-card-title {
  color: #bb1d1d;
}

.title_span{
  border-bottom: 1px solid #e5e5e5;
  margin-left: 12px;
  padding-right: 20px;
}

.ct-series-a .ct-bar, .ct-series-a .ct-line, .ct-series-a .ct-point, .ct-series-a .ct-slice-donut {
  stroke: green !important;
}
.ct-series-b .ct-bar, .ct-series-b .ct-line, .ct-series-b .ct-point, .ct-series-b .ct-slice-donut {
  stroke: #d70206!important;
}

.ct-series-d .ct-bar, .ct-series-d .ct-line, .ct-series-d .ct-point, .ct-series-d .ct-slice-donut {
  stroke: #807e7d !important;
}
</style>
