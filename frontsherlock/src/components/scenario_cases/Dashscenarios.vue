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
            <span @click="fecthCases(scenario.id)" style="cursor: pointer; width: 100%">{{ scenario.name }} <br>
          </span>
          <div v-if="scenario.state_code === 'DISABLE'" class="uk-badge uk-label">Disabled</div>
            <hr>
          </div>
          <div class="uk-width-1-5">
            <ul class="uk-iconnav">
                <li> <a @click="fecthCases(scenario.id)" uk-icon="icon: chevron-right;"></a></li>
                <li v-show="scenario.state_code === 'ACTIVE'"> <a @click="disableScenario(scenario.id)" uk-icon="icon: lock"></a></li>
                <li v-show="scenario.state_code === 'DISABLE'"> <a @click="enableScenario(scenario.id)" uk-icon="icon: unlock"></a></li>
                <li><a @click="editScenario(scenario.name, scenario.id)" uk-icon="icon: file-edit"></a></li>
                <li><a @click="removeScenario(scenario.id)" uk-icon="icon: trash"></a></li>
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
            Scenario: {{ scenarioFull.scenario_name }}
             <div v-if="scenarioFull.scenario_state === 'DISABLE'" class="uk-badge uk-label">Disabled</div>

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
                    <li v-show="tstcase.state_code === 'ACTIVE'"> <a @click="disableCase(tstcase.id)" uk-icon="icon: lock"></a></li>
                    <li v-show="tstcase.state_code === 'DISABLE'"> <a @click="enableCase(tstcase.id)" uk-icon="icon: unlock"></a></li>
                    <li><a @click="editCase(tstcase.name, scenarioFull.scenario_id, tstcase.id )"uk-icon="icon: file-edit"></a></li>
                    <li><a @click="removeCase(tstcase.id)" uk-icon="icon: trash"></a></li>
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
        <br><br><router-link class="uk-button uk-button-default" style='margin-top:10px;' :to="{ path: '/project/view/'+ this.projectId }">Return to DashBoard</router-link>
        <br>
        <hr>
        <h3> info </h3>
        - After typing the test case, you can hit keyword "shift + enter" on your keyboard and it will be saved automactily
        <br><br>
        - If you wish to edit a scenario or  case, just click on the edit button <a uk-icon="icon: file-edit"></a>.
        <br><br>
        - Blocking a Scenario or a Case will block on the current cycle and all the coming cycles.
        <br><br>
        - Blocking or removing a scenario will block / delete all their test cases.
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
    fetchScenarios (e) {
      this.$http.get('scenario/project_scenarios/' + this.projectId).then(function (response) {
        this.loading = false
        this.scenarios = response.body
        this.scenarios = this.scenarios.reverse()
      })
    },
    addNewScenario () {
      if (this.newScenario === '') {
        UIkit.notification('The scenario can`t be blank', {status: 'warning'}, {timeout: '700'})
      } else {
        var scenario = {
          'scenario_name': this.newScenario,
          'projectId': this.$route.params.projectId
        }
        this.$http.post('scenario/new', scenario).then(function (response) {
          this.newScenario = ''
          UIkit.notification('<span uk-icon="icon: check"></span> Scenario Created', {timeout: '700'})
        })
      }
    },
    addNewCase () {
      if (this.newCase === '') {
        UIkit.notification('The case can`t be blank', {status: 'warning'}, {timeout: '700'})
      } else {
        var tstcase = {
          'case_name': this.newCase
        }
        this.$http.post('scenarios/' + this.scenarioFull.scenario_id + '/tst_case/new', tstcase).then(function (response) {
          this.newCase = ''
          UIkit.notification('<span uk-icon="icon: check"></span> Case Created', {timeout: '700'})
          this.fecthCases(this.scenarioFull.scenario_id)
        })
      }
    },
    editScenario (scenarioName, scenarioId) {
      var vueInstance = this
      UIkit.modal.prompt('Edit Scenario:', scenarioName).then(function (newScenarioName) {
        if (scenarioName === '') {
          UIkit.notification('<span uk-icon="icon: ban"></span> Scenario can`t be blank', {timeout: '700'})
          return
        } else if (newScenarioName === null) {
          return
        }
        vueInstance.$http.post('scenario/edit', {'scenario_id': scenarioId, 'scenario_name': scenarioName})
        .then(function (response) {
          UIkit.notification('<span uk-icon="icon: check"></span> Scenario Edited', {timeout: '700'})
          this.fetchScenarios()
        })
      }, function () {
        return
      })
    },
    editCase (caseName, scenarioId, caseId) {
      var vueInstance = this
      UIkit.modal.prompt('Edit Test Case:', caseName).then(function (caseName) {
        if (caseName === '') {
          UIkit.notification('<span uk-icon="icon: ban"></span>Test Case can`t be blank', {timeout: '700'})
          return
        } else if (caseName === null) {
          return
        }
        vueInstance.$http.post('scenarios/' + scenarioId + '/tst_case/edit', {'case_id': caseId, 'case_name': caseName})
        .then(function (response) {
          UIkit.notification('<span uk-icon="icon: check"></span> Test Case Edited', {timeout: '700'})
          this.fecthCases(this.scenarioFull.scenario_id)
        })
      }, function () {
        return
      })
    },
    removeScenario (scenarioId) {
      var vueInstance = this
      UIkit.modal.confirm('If you remove this scenario, You will not be able to recover it. Click OK to confirm the operation.').then(function () {
        vueInstance.$http.post('scenario/change_status', {'scenario_id': scenarioId, 'action': 'REMOVE'}).then(function (response) {
          UIkit.notification('<span uk-icon="icon: trash"></span> Scenario Removed', {timeout: '700'})
        })
      }, function () {
      })
    },
    disableScenario (scenarioId) {
      var vueInstance = this
      UIkit.modal.confirm('Do you want to disable this scenario? It will not be available for the next cycle.').then(function () {
        vueInstance.$http.post('scenario/change_status', {'scenario_id': scenarioId, 'action': 'DISABLE'}).then(function (response) {
          UIkit.notification('<span uk-icon="icon: lock"></span> Scenario Disabled', {timeout: '700'})
        })
      }, function () {
      })
    },
    enableScenario (scenarioId) {
      var vueInstance = this
      UIkit.modal.confirm('Please confirm the Scenario activation.').then(function () {
        vueInstance.$http.post('scenario/change_status', {'scenario_id': scenarioId, 'action': 'ENABLE'}).then(function (response) {
          UIkit.notification('<span uk-icon="icon: unlock"></span> Scenario Enabled', {timeout: '700'})
        })
      }, function () {
      })
    },
    disableCase (caseId) {
      var vueInstance = this
      UIkit.modal.confirm('Do you want to disable this Test Case? It will not be available for the next cycle.').then(function () {
        vueInstance.$http.post('scenarios/' + vueInstance.scenarioFull.scenario_id + '/tst_case/change_status', {'case_d': caseId, 'action': 'DISABLE'}).then(function (response) {
          UIkit.notification('<span uk-icon="icon: lock"></span> Test Case Disabled', {timeout: '700'})
          this.fecthCases(vueInstance.scenarioFull.scenario_id)
        })
      }, function () {
      })
    },
    enableCase (caseId) {
      var vueInstance = this
      UIkit.modal.confirm('Please confirm the Test Case activation.').then(function () {
        vueInstance.$http.post('scenarios/' + vueInstance.scenarioFull.scenario_id + '/tst_case/change_status', {'case_id': caseId, 'action': 'ENABLE'}).then(function (response) {
          if (response.message === 'SCENARIO_DISABLED') {
            UIkit.notification('<span uk-icon="icon: ban"></span> This Case Scenario is disabled!', {timeout: '700'})
            return
          }
          UIkit.notification('<span uk-icon="icon: unlock"></span> Test Case Enabled', {timeout: '700'})
          this.fecthCases(vueInstance.scenarioFull.scenario_id)
        })
      }, function () {
      })
    },
    fecthCases (scenarioId) {
      this.loading = true
      this.$http.get('scenario/cases/' + scenarioId).then(function (response) {
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
    this.fetchScenarios()

    this.interval = setInterval(function () {
      this.fetchScenarios()
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
