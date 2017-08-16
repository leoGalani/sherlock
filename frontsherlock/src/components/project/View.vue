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
                <h3 v-if="project.last_cycle.state_code === 'active'">Current cycle stats</h3>
                <h3 v-else>Resume of Last Cycle</h3>
                <div class="ct-chart">
                  <div v-if="display_load_chart">
                    <div uk-spinner></div>
                    Loading chart
                  </div>
                </div>
                <router-link v-if="project.last_cycle.state_code === 'active'" class="uk-button uk-button-default" style='margin-top:10px;' :to="{ name: 'project_cycles', params: {projectId: this.projectId, cycleId: this.current_cycle.id} }">Execute Test Cases</router-link>
                <a v-if="project.last_cycle.state_code === 'active'" class="uk-button uk-button-default" style='margin-top:10px;' @click="checkCloseCyle(project.last_cycle.id)">Close Cycle</a>
                <a v-if="project.last_cycle.state_code === 'closed'" @click="createCycle()" class="uk-button uk-button-default"> Create New Cycle</a>
                <router-link v-if="project.last_cycle.state_code === 'closed'" class="uk-button uk-button-default" :to="{ path: '/project/view/'+projectId+'/scenario_cases' }">Manage Scenarios and Test Cases</router-link>
              </div>
              <div class="uk-width-2-5">
                <h3>Cycle {{this.current_cycle.cycle}} status </h3>

                <div class="uk-grid-divider uk-child-width-expand@s" uk-grid style="margin-top:20px !important">
                  <div>
                      <div class="uk-form-label" style="font-weight: 800;">created at:</div>
                      <div>
                        {{this.current_cycle.created_at}} <a title="dd-mm-yyyy" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: question"></a>
                    </div>
                  </div>
                  <div v-if="project.last_cycle.state_code === 'closed'">
                      <div class="uk-form-label" style="font-weight: 800;">closed at:</div>
                      <div>
                        {{this.current_cycle.closed_at}} <a title="dd-mm-yyyy" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: question"></a>
                    </div>
                  </div>
                </div>

                <div v-if="project.last_cycle.state_code === 'closed'" class="uk-grid-divider uk-child-width-expand@s" uk-grid style="margin-top:20px !important">
                  <div>
                      <div class="uk-form-label" style="font-weight: 800;">closed by:</div>
                      <div>
                        {{this.current_cycle.closed_by}}
                    </div>
                  </div>
                  <div v-if="project.last_cycle.state_code === 'closed'">
                      <div class="uk-form-label" style="font-weight: 800;">reason:</div>
                      <div  style="max-height: 137px; white-space: normal" class="hide_overflow">
                        {{this.current_cycle.closed_reason}}</a>
                    </div>
                  </div>
                </div>

                <div class="uk-grid-divider uk-child-width-expand@s" uk-grid style="margin-top:20px !important">
                  <div>
                      <div class="uk-form-label" style="font-weight: 800;">cases not executed:</div>
                      <div>
                        {{this.current_cycle.stats.total_not_executed}}
                    </div>
                  </div>
                  <div>
                      <div class="uk-form-label" style="font-weight: 800;">cases passed:</div>
                      <div>
                        {{this.current_cycle.stats.total_passed}}</a>
                    </div>
                  </div>
                </div>

                <div class="uk-grid-divider uk-child-width-expand@s" uk-grid style="margin-top:20px !important">
                  <div>
                      <div class="uk-form-label" style="font-weight: 800;">cases failed:</div>
                      <div>
                        {{this.current_cycle.stats.total_error}}
                    </div>
                  </div>
                  <div>
                      <div class="uk-form-label" style="font-weight: 800;">cases blocked:</div>
                      <div>
                        {{this.current_cycle.stats.total_blocked}}</a>
                    </div>
                  </div>
                </div>
                <br>
              </div>
          </div>
          <hr>
          <div v-if="project.have_cycles">
            <div class="ct-chart-line-legendnames" v-if="this.current_cycle.cycle >= 2">
              <div v-if="display_load_chart">
                <div uk-spinner></div>
                Loading chart
              </div>
            </div>
          </div>
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
require('chartist-plugin-legend')

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
          UIkit.notification('Project Not Found.', {status: 'danger', timeout: '700'})
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
            } else if (response.body.message === 'NO_TEST_SCENARIOS') {
              UIkit.notification('<span uk-icon="icon: ban"></span> Sorry but there is no active Test Case for the next cycle', {timeout: '700'})
            } else {
              console.log(response.body.message)
              UIkit.notification('<span uk-icon="icon: ban"></span> Please close the current cycle', {timeout: '700'})
            }
          })
        }, function () {
          return
        })
      }
    },
    checkCloseCyle (cycleID) {
      var notExecuted = this.current_cycle.stats.total_not_executed
      var vueInstance = this
      if (notExecuted > 0) {
        UIkit.modal.confirm('This cycle still have [' + notExecuted.toString() + '] not executed. Are you sure!?').then(function () {
          UIkit.modal.prompt('Please provide a reason why closing the cycle with not executed tests? (required):', '').then(function (reason) {
            if (reason === null || reason === '') {
              UIkit.notification('<span uk-icon="icon: ban"></span> You should provide a reason', {timeout: '700'})
              return
            } else {
              vueInstance.closeCycle(cycleID, reason)
            }
          })
        }, function () {
        })
      } else {
        vueInstance.closeCycle(cycleID, 'normal cycle end')
      }
    },
    closeCycle (cycleID, reason) {
      this.$http.post('projects/' + this.projectId + '/cycle/close/' + cycleID, {'reason': reason}).then(function (response) {
        if (response.body.message === 'CYCLE_CLOSED') {
          UIkit.notification('<span uk-icon="icon: check"></span> Cycle Closed', {timeout: '700'})
        }
      })
    },
    mountChartCurrentCycle () {
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
    },
    mountChartResume () {
      if (this.project.have_cycles) {
        this.$http.get('projects/' + this.projectId + '/cycle/timeline').then(function (response) {
          Chartist.Line('.ct-chart-line-legendnames', {
            labels: response.body.cycles_number,
            series: [
              response.body.cycles_passed,
              response.body.cycles_failed,
              response.body.cycles_blocked,
              response.body.cycles_not_executed
            ]
          }, {
            fullWidth: true,
            height: '300px',
            chartPadding: {
              right: 40
            },
            plugins: [
              Chartist.plugins.legend({
                legendNames: ['Passed', 'Failed', 'Blocked', 'Not Executed']
              })
            ]
          })
        })
      }
    }
  },
  created: function () {
    this.projectId = this.$route.params.projectId
    this.fetchProject(this.$route.params.projectId)
  },
  mounted: function () {
    this.mountChartCurrentCycle()
    this.mountChartResume()
    this.interval = setInterval(function () {
      this.fetchProject(this.$route.params.projectId)
      this.mountChartCurrentCycle()
      this.mountChartResume()
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
