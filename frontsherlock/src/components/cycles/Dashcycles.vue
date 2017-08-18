<template>
  <div class="dashboard uk-grid">
    <div  id="loading" v-if="loading">
       <center><div uk-spinner></div>
       Loading...</center>
     </div>
    <div class="uk-width-4-5">
      <ul uk-tab="animation: uk-animation-slide-left-medium, uk-animation-slide-right-medium" id='cenarios_cases'>
        <li><a href="#">Scenarios</a></li>
        <li><a href="#" v-if="caseslodaded">Cases</a></li>
      </ul>

<ul class="uk-switcher uk-margin" id='cenarios_cases'>
    <li>
      <div class="content scenario">
      <div v-for="scenario in scenarios" :key="scenario.scenario_id" v-if="scenario.cases_stats.total > 0"class="uk-grid ">
          <div @click="fetchCycleCases(scenario.scenario_id)" class="uk-width-4-5" style="cursor: pointer; width: 77% !important;">
            <span>{{ scenario.scenario_name }} <br>
          </span>
            <hr>
          </div>
          <div class="uk-width-1-5" style="width: 23% !important;">
            <ul class="uk-iconnav">
                <li style="padding-left: 8px !important;">
                  <a @click="fetchCycleCases(scenario.scenario_id)" uk-icon="icon: chevron-right;" title="Access Test Cases" uk-tooltip="delay: 300; pos: bottom"></a></li>
                <li style="padding-left: 8px !important;">
                  <span class="uk-badge passed">
                    <a style="color: white !important; cursor: default !important;" title="Cases Passed" uk-tooltip="delay: 300; pos: bottom ">
                      {{scenario.cases_stats.total_passed}}
                    </a>
                  </span>
                </li>
                <li style="padding-left: 8px !important;">
                  <span class="uk-badge failed">
                    <a style="color: white !important; cursor: default !important;" title="Cases Failed" uk-tooltip="delay: 300; pos: bottom ">
                      {{scenario.cases_stats.total_error}}
                    </a>
                  </span>
                </li>
                <li style="padding-left: 8px !important;">
                  <span class="uk-badge blocked">
                    <a style="color: white !important; cursor: default !important;" title="Cases Blocked" uk-tooltip="delay: 300; pos: bottom ">
                      {{scenario.cases_stats.total_blocked}}
                    </a>
                  </span>
                </li>
                <li style="padding-left: 8px !important;">
                  <span class="uk-badge">
                    <a style="color: white !important; cursor: default !important;" title="Cases Not Executed" uk-tooltip="delay: 300; pos: bottom ">
                      {{scenario.cases_stats.total_not_executed}}
                    </a>
                  </span>
                </li>
            </ul>
          </div>
      </div>
    </div>
    </li>
    <li>
        <h3 v-if="! caseslodaded">
          Nothing to see here... <br>
          Please click on any scenario to load the cases.
        </h3>
        <div v-else>
          <h4 class="scenario_name_case">
            Scenario: {{ scenarioFull.scenario_name }} <br>
          </h4>
          <div class="content scenario">
            <div v-for="tstcase in tstcases" :key="tstcase.case_id" class="uk-grid">
              <div class="uk-width-4-5">
                <span> {{ tstcase.case_name }} </span>
              </span>
              <hr>
              </div>
              <div class="uk-width-1-5">
                <ul class="uk-iconnav">
                    <li> <a title="Pass" uk-tooltip="delay: 300; pos: bottom"
                      @click="changeCaseStatus(tstcase.case_id, scenarioFull.scenario_id, 'passed')">
                      <span v-show="tstcase.case_cycle_state === 'passed'" uk-icon="icon: check" class='passed'></span>
                      <span v-show="tstcase.case_cycle_state !== 'passed'" uk-icon="icon: check"></span>
                      </a></li>
                    <li> <a title="Fail" uk-tooltip="delay: 300; pos: bottom"
                      @click="changeCaseStatus(tstcase.case_id, scenarioFull.scenario_id, 'error')">
                      <span v-show="tstcase.case_cycle_state === 'error'" uk-icon="icon: ban" class='failed'></span>
                      <span v-show="tstcase.case_cycle_state !== 'error'" uk-icon="icon: ban"></span>
                    </a></li>
                    <li> <a title="Block" uk-tooltip="delay: 300; pos: bottom"
                      @click="changeCaseStatus(tstcase.case_id, scenarioFull.scenario_id, 'blocked')">
                      <span v-show="tstcase.case_cycle_state === 'blocked'" uk-icon="icon: lock" class='blocked'></span>
                      <span v-show="tstcase.case_cycle_state !== 'blocked'" uk-icon="icon: lock"></span>
                    </a></li>
                    <li> <a title="Reset Status" uk-tooltip="delay: 300; pos: bottom"
                      @click="changeCaseStatus(tstcase.case_id, scenarioFull.scenario_id, 'not_executed')">
                      <span uk-icon="icon: reply"></span>
                    </a></li>
                </ul>
              </div>
            </div>
          </div>
      </div>
    </li>
</ul>

</div>
    <div class="uk-width-1-5">
      <div class="info" style="z-index: 980;" uk-sticky="bottom: true">
        <br><br><router-link class="uk-button uk-button-default" style='margin-top:10px;' :to="{ path: '/project/view/'+ this.projectId }">Return to DashBoard</router-link>
        <br>
        <hr>
        <h3> info </h3>
        - If you disabled a case test, it will not appear here.
      </div>
    </div>
  </div>
</template>

<script>
import UIkit from 'uikit'

export default {
  name: 'dashboard',
  data () {
    return {
      projectId: this.$route.params.projectId,
      cycleId: this.$route.params.cycleId,
      scenarios: [],
      scenarioFull: '',
      tstcases: [],
      newScenario: '',
      newCase: '',
      loading: false,
      caseslodaded: false,
      viewcase: false
    }
  },
  methods: {
    fetchCycleScenarios () {
      this.$http.get('projects/' + this.projectId + '/cycle/get_scenarios_for_cyle/' + this.cycleId).then(function (response) {
        this.loading = false
        this.scenarios = response.body
        this.scenarios = this.scenarios.reverse()
      })
    },
    changeCaseStatus (caseId, scenarioId, status) {
      this.$http.post('projects/' + this.projectId + '/cycle/change_case_state_code', {'case_id': caseId, 'cycle_id': this.cycleId, 'action': status})
      .then(function (response) {
        this.fetchCycleCases(scenarioId)
      })
    },
    fetchCycleCases (scenarioId) {
      this.loading = true
      this.$http.get('projects/' + this.projectId + '/cycle/get_cases_for_cyle/' + this.cycleId + '/scenario/' + scenarioId).then(function (response) {
        this.loading = false
        this.caseslodaded = true
        this.scenarioFull = response.body
        this.tstcases = this.scenarioFull.cases.reverse()
        UIkit.tab('#cenarios_cases', {'animation': 'uk-animation-middle-left'}).show(1)
      })
    },
    cleanCases () {
      this.caseslodaded = false
      this.scenarioFull = []
      this.tstcases = []
    }
  },
  created: function () {
    this.loading = true
    this.fetchCycleScenarios()

    this.interval = setInterval(function () {
      this.fetchCycleScenarios()
    }.bind(this), 2000)
  },
  updated: function () {
  },
  beforeDestroy: function () {
    clearInterval(this.interval)
  }
}
</script>

<style scoped>

.dashboard{
  padding: 15px;
}

.content{
  min-height: 400px;
  overflow-x: hidden;
  padding: 10px;
  width: 100%;
}

.info{
  width:90%;
  margin-top: 10px;
}

ol, ul {
    padding-left: 5px;
    list-style: none;
}

ul li {
  padding-bottom: 10px;
  padding-top: 10px;
}

.uk-tab>*>a {
    text-transform: capitalize;
    font-size: 25px;
}

.uk-tab>.uk-active>a {
    border-color: #ffa500;
    font-size: 25px;
  }

.divider_new_scenario{
  border-top: 1px solid orange;
  opacity: 0.5;
  width: 50%;
}

.uk-iconnav{
  float: right;
}

.scenario_name_case{
  border: 1px solid orange;
  text-align: center;
  padding: 10px;
}

.uk-badge {
    margin: 0px;
    padding: 0px 7px;
}

.passed {
  background: green;
  color: white !important;
  stroke: white !important;
  border-radius: 16px;
}

.failed {
  background-color: #e80303;
  color: white !important;
  stroke: white !important;
  border-radius: 16px;
}

.blocked {
  background-color: orange;
  color: whitesmoke !important;
  stroke: whitesmoke !important;
  border-radius: 16px;
}
</style>
