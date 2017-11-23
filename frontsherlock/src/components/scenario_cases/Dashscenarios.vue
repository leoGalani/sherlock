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
      <div class="uk-form-controls">
        <div class="uk-inline">
            <a class="uk-form-icon uk-form-icon-flip" @click="addNewScenario" uk-icon="icon: arrow-right"></a>
            <textarea class="uk-textarea uk-width-1-1 input_text"
            placeholder="Enter you new scenario and press shift + enter to save it" type="textarea"
            v-model="newScenario" @keyup.shift.enter="addNewScenario">
          </textarea>
        </div>
        <center style="padding-top: 17px;"> <hr class="divider_new_scenario"> </center>
      </div>

      <div class="content scenario">
        <div v-if="!scenarios.length">
          <center>
            <img class="logo_menu" src='../../assets/img/sherlock_butterfly.png'>
              </center>
        </div>
      <div v-for="scenario in scenarios" :key="scenario.id" class="uk-grid ">
          <div class="uk-width-4-5">
            <span @click="fecthCases(scenario.id)" style="cursor: pointer; width: 100%">{{ scenario.name }} <br>
          </span>
          <br>
          <span>
            <a uk-icon="icon: tag" style="margin-right:10px" uk-toggle="target: + input; animation: uk-animation-fade"
            title="Manage Scenario Tags" uk-tooltip="delay: 300; pos: bottom"></a>
              <input v-bind:id="'tag_'+scenario.id" type="text" class="uk-input" placeholder="Use space to separete tags"
              style="width: 268px; height: 25px; font-size: 13px;" hidden @keyup.space="addScenarioTag(scenario.id, $event.target.value); $event.target.value = ''"
              @keyup.enter="addScenarioTag(scenario.id, $event.target.value); $event.target.value = ''">
            <span v-for="tag in scenario.tags" class="uk-label"> #{{tag.tag}}
            <span uk-icon="icon: close; ratio: 0.6" style="stroke: white !important; margin-left: 5px;"
            @click="removeScenarioTag(tag.id, tag.scenario_id)"></span>
          </span>
            <span v-if="scenario.state_code === 'disable'" class="uk-label">Disabled</span>
          </span>


            <hr>
          </div>
          <div class="uk-width-1-5">
            <ul class="uk-iconnav">
                <li> <a @click="fecthCases(scenario.id)" uk-icon="icon: chevron-right;" title="Load Scenario Cases" uk-tooltip="delay: 300; pos: bottom"></a></li>
                <li v-show="scenario.state_code === 'active'"> <a @click="disableScenario(scenario.id)"
                  title="Disable Scenario" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: lock"></a></li>
                <li v-show="scenario.state_code === 'disable'"> <a @click="enableScenario(scenario.id)"
                  title="Enable Scenario" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: unlock"></a></li>
                <li><a @click="editScenario(scenario.name, scenario.id)"
                  title="Edit Scenario" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: file-edit"></a></li>
                <li><a @click="removeScenario(scenario.id)"
                  title="Remove Scenario and Cases" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: trash"></a></li>
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
             <div v-if="scenarioFull.scenario_state === 'disable'" class="uk-badge uk-label">Disabled</div>

          </h4>
          <div class="uk-form-controls">
            <div v-if="scenarioFull.scenario_state === 'active'" class="uk-inline">
              <a class="uk-form-icon uk-form-icon-flip" @click="addNewCase" uk-icon="icon: arrow-right"></a>
              <textarea class="uk-textarea uk-width-1-1 input_text"
              placeholder="Enter a new test case" type="textarea"
              v-model="newCase" @keyup.shift.enter="addNewCase">
            </textarea>
            </div>
            <center style="padding-top: 30px;"> <hr class="divider_new_scenario"> </center>
          </div>

          <div class="content scenario">
            <div v-if="!tstcases.length">

              <center>
                <img class="logo_menu" src='../../assets/img/sherlock_butterfly.png'>
                  </center>
            </div>
            <div v-for="tstcase in tstcases" :key="tstcase.id" class="uk-grid">
              <div class="uk-width-4-5">
                <span> {{ tstcase.name }} </span>
              </span><br><br>
              <span>
                <a uk-icon="icon: tag" style="margin-right:10px" uk-toggle="target: + input; animation: uk-animation-fade"
                title="Manage Scenario Tags" uk-tooltip="delay: 300; pos: bottom"></a>
                  <input v-bind:id="'tag_'+tstcase.id" type="text" class="uk-input" placeholder="Use space to separete tags"
                  style="width: 268px; height: 25px; font-size: 13px;" hidden @keyup.space="addCaseTag(tstcase.id, $event.target.value); $event.target.value = ''"
                  @keyup.enter="addCaseTag(tstcase.id, $event.target.value); $event.target.value = ''">
                <span v-for="tag in tstcase.tags" class="uk-label"> #{{tag.tag}}
                <span uk-icon="icon: close; ratio: 0.6" style="stroke: white !important; margin-left: 5px;"
                @click="removeCaseTag(tag.id, tag.case_id)"></span>
              </span>
            </span>
              <div v-if="tstcase.state_code === 'disable'" class="uk-badge uk-label">Disabled</div>
                <hr>
              </div>
              <div class="uk-width-1-5">
                <ul class="uk-iconnav">
                    <li v-show="tstcase.state_code === 'active'"> <a @click="disableCase(tstcase.id)"
                      title="Disable Case" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: lock"></a></li>
                    <li v-show="tstcase.state_code === 'disable'"> <a @click="enableCase(tstcase.id)"
                      title="Enable Case" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: unlock"></a></li>
                    <li><a @click="editCase(tstcase.name, scenarioFull.scenario_id, tstcase.id )"
                      title="Edit Case" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: file-edit"></a></li>
                    <li><a @click="removeCase(tstcase.id)"
                      title="Remove Case" uk-tooltip="delay: 300; pos: bottom" uk-icon="icon: trash"></a></li>
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
      viewcase: false,
      tag_field: ''
    }
  },
  methods: {
    fetchScenarios () {
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
        if (newScenarioName === '') {
          UIkit.notification('<span uk-icon="icon: ban"></span> Scenario can`t be blank', {timeout: '700'})
          return
        } else if (newScenarioName === null) {
          return
        }
        vueInstance.$http.post('scenario/edit', {'scenario_id': scenarioId, 'scenario_name': newScenarioName})
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
        vueInstance.$http.post('scenarios/' + vueInstance.scenarioFull.scenario_id + '/tst_case/change_status', {'case_id': caseId, 'action': 'DISABLE'}).then(function (response) {
          UIkit.notification('<span uk-icon="icon: lock"></span> Test Case Disabled', {timeout: '700'})
          this.fecthCases(vueInstance.scenarioFull.scenario_id)
        })
      }, function () {
      })
    },
    removeCase (caseId) {
      var vueInstance = this
      UIkit.modal.confirm('Do you want to remove this Test Case? This process is not reversable.').then(function () {
        vueInstance.$http.post('scenarios/' + vueInstance.scenarioFull.scenario_id + '/tst_case/change_status', {'case_id': caseId, 'action': 'REMOVE'}).then(function (response) {
          UIkit.notification('<span uk-icon="icon: ban"></span> Test Case Removed', {timeout: '700'})
          this.fecthCases(vueInstance.scenarioFull.scenario_id)
        })
      }, function () {
      })
    },
    enableCase (caseId) {
      var vueInstance = this
      UIkit.modal.confirm('Please confirm the Test Case activation.').then(function () {
        vueInstance.$http.post('scenarios/' + vueInstance.scenarioFull.scenario_id + '/tst_case/change_status', {'case_id': caseId, 'action': 'ENABLE'}).then(function (response) {
          if (response.body.message === 'SCENARIO_DISABLED') {
            UIkit.notification('<span uk-icon="icon: ban"></span> This Case Scenario is disabled!', {timeout: '700'})
            return
          } else if (response.body.message === 'DONE') {
            UIkit.notification('<span uk-icon="icon: unlock"></span> Test Case Enabled', {timeout: '700'})
            this.fecthCases(vueInstance.scenarioFull.scenario_id)
          } else {
            UIkit.notification('<span uk-icon="icon: ban"></span> Something Wrong Happend.', {timeout: '700'})
            return
          }
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
    addScenarioTag (ScenarioId, value) {
      var url = 'scenario/register_tag'
      let newTag = {
        tag: value,
        scenario_id: ScenarioId
      }
      this.$http.post(url, newTag).then(function (response) {
        if (response.body.message === 'TAG_CREATED') {
          this.fetchScenarios()
        }
      })
    },
    removeScenarioTag (tagId, scenarioId) {
      var url = 'scenario/remove_tag'
      let tag = {
        tag_id: tagId,
        scenario_id: scenarioId
      }
      for (var i = 0; i < this.scenarios.length; i++) {
        for (var j = 0; j < this.scenarios[i].tags.length; j++) {
          if (this.scenarios[i].tags[j].id === tagId) {
            var index = this.scenarios[i].tags.indexOf(this.scenarios[i].tags[j].tag)
            this.scenarios[i].tags.splice(index, 1)
          }
        }
      }
      this.$http.post(url, tag).then(function (response) {
        if (response.body.message === 'TAG_REMOVED') {
          this.fetchScenarios()
        }
      })
    },
    addCaseTag (CaseId, value) {
      var url = 'scenarios/' + this.scenarioFull.scenario_id + '/tst_case/register_tag'
      let newTag = {
        tag: value,
        case_id: CaseId
      }
      this.$http.post(url, newTag).then(function (response) {
        if (response.body.message === 'TAG_CREATED') {
          this.fecthCases(this.scenarioFull.scenario_id)
        }
      })
    },
    removeCaseTag (tagId, caseId) {
      var url = 'scenarios/' + this.scenarioFull.scenario_id + '/tst_case/remove_tag'
      let tag = {
        tag_id: tagId,
        case_id: caseId
      }
      for (var i = 0; i < this.tstcases.length; i++) {
        for (var j = 0; j < this.tstcases[i].tags.length; j++) {
          if (this.tstcases[i].tags[j].id === tagId) {
            var index = this.tstcases[i].tags.indexOf(this.tstcases[i].tags[j].tag)
            this.tstcases[i].tags.splice(index, 1)
          }
        }
      }
      this.$http.post(url, tag).then(function (response) {
        if (response.body.message === 'TAG_REMOVED') {
          this.fecthCases(this.scenarioFull.scenario_id)
        }
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

.input_text {
    width: 96% !important;
}

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

.uk-inline {
  width: 100%
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

.uk-label{
  font-size: 12px;
  padding: 0 10px;
  margin: 0 3px;
}

</style>
