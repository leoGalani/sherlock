<template>
  <div class="dashboard uk-grid">
    <div  id="loading" v-if="loading">
       <center><div uk-spinner></div>
       Loading...</center>
     </div>
    <div class="uk-width-4-5">
      <ul uk-tab="animation: uk-animation-slide-left-medium, uk-animation-slide-right-medium" id='cenarios_cases'>
        <li><a href="#">Scenarios</a></li>
        <li><a href="#">Cases</a></li>
      </ul>

<ul class="uk-switcher uk-margin" id='cenarios_cases'>
    <li>
      <div class="uk-form-controls">
          <textarea class="uk-textarea uk-width-1-1"
          placeholder="Enter a new scenario description" type="textarea"
          v-model="newScenario" @keyup.shift.enter="addNewScenario">
        </textarea>
        <center style="padding-top: 17px;"> <hr class="divider_new_scenario"> </center>
      </div>

      <div class="content scenario">
      <div v-for="scenario in scenarios" :key="scenario.id" class="uk-grid ">
          <div class="uk-width-4-5">
            <span @click="removeScenario(scenario.id)">{{ scenario.name }} <br>
          </span>
          <div v-if="scenario.state_code === 'DISABLE'" class="uk-badge uk-label">Disabled</div>
            <hr>
          </div>
          <div class="uk-width-1-5">
            <ul class="uk-iconnav">
                <li> <a @click="fecthCases(scenario.id)" uk-icon="icon: chevron-right;"></a></li>
            </ul>
          </div>
      </div>
    </div>
    </li>
    <li>
        <h3 v-if="! caseslodaded">
          Nothing to see here... <br>
          Please click on any Scenario to load or create cases for them.
        </h3>
        <div v-else>
          <h4 class="scenario_name_case">
            Scenario: {{ scenarioFull.scenario_name }} <br>
          </h4>
          <div class="uk-form-controls">
              <textarea class="uk-textarea uk-width-1-1"
              placeholder="Enter a new test case" type="textarea"
              v-model="newCase" @keyup.shift.enter="addNewCase">
            </textarea>
            <center style="padding-top: 30px;"> <hr class="divider_new_scenario"> </center>
          </div>

          <div class="content scenario">
            <div v-for="tstcase in tstcases" :key="tstcase.id" class="uk-grid">
              <div class="uk-width-4-5">
                <span> {{ tstcase.name }} </span>
              </span>
              <div v-if="tstcase.state_code === 'DISABLE'" class="uk-badge uk-label">Disabled</div>
                <hr>
              </div>
              <div class="uk-width-1-5">
                <ul class="uk-iconnav">
                    <li> <a @click="approveCase(tstcase.id)" uk-icon="icon: lock"></a></li>
                </ul>
              </div>
            </div>
          </div>
      </div>
    </li>
</ul>

</div>
    <div class="uk-width-1-5">
      <div class="info">
        <h3> info </h3>
        - After typing the test case, you can hit keyword "shift + enter" on your keyboard and it will be saved automactily
        <br><br>
        - If you wish to edit a scenario or  case, just click on the edit button <a uk-icon="icon: file-edit"></a>.
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
      project_id: this.$route.params.projectId,
      cycle_id: this.$route.params.cycleId,
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
    fetchCycleScenarios (e) {
      this.$http.get('scenario/project_scenarios/' + this.project_id).then(function (response) {
        this.loading = false
        this.scenarios = response.body
        this.scenarios = this.scenarios.reverse()
      })
    },
    approveCase (caseId) {
      var vueInstance = this
      vueInstance.$http.post('projects/' + this.projectId + '/cycle/' + this.cycleId + '/change_case_state', {'case_id': caseId, 'action': 'PASSED'})
      .then(function (response) {
      })
    },
    fecthCycleHistory () {
      this.loading = true
      this.$http.get('scenario/cases/' + 0).then(function (response) {
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
    this.fecthCycleHistory()

    this.interval = setInterval(function () {
      this.fecthCycleHistory()
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

.uk-badge {
  background: #788b9e !important;
  margin: 10px;
}

.scenario_name_case{
  border: 1px solid orange;
  text-align: center;
  padding: 10px;
}

</style>
