<template>
  <div class="dashboard">
    <div  id="loading" v-if="loading">
       <center><div uk-spinner></div>
       Loading...</center>
     </div>

     <div class="uk-grid" v-if="showTitle">
       <div class="uk-width-4-5" style="width:65% !important">
         <h2 style="margin-left: 18px;"> Current Projects </h2>
       </div>
       <div class="uk-width-1-5" style="width:35% !important; text-align: right; padding-right: 14px;">
         <span><i class="material-icons">filter_list</i></span>
         <span>
         <a class="uk-button  uk-button-default filter_state"
            v-bind:class="{ filter_state_active: filterActive }"
            @click="filterActive = !filterActive, filterClick('active')"> active </a>
         <a class="uk-button uk-button-default filter_state"
            v-bind:class="{ filter_state_active: filterClose }"
            @click="filterClose = !filterClose, filterClick('closed')""> closed </a>
         <a class="uk-button uk-button-default filter_state"
            v-bind:class="{ filter_state_active: filterNoCycle }"
            @click="filterNoCycle = !filterNoCycle, filterClick('nocycle')""> no cycle </a>
       </span>
       </div>
     </div>


    <transition-group>
    <div v-for="project in projects.projects" :key="project.id" class="project_box" v-if="filter.length === 0 || filter.indexOf(project.cycle_state) > -1">
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
  </transition-group>

    <div v-if="showGreetings">
      <hr>
      <h2 style="margin-left:20px"><span class="uk-margin-small-right" uk-icon="icon: heart"></span> Hey, this seems like a brand new installation! thanks for giving sherlock a try! <span class="uk-margin-small-right" uk-icon="icon: heart"></span></h2>

      <p style="margin-left:20px"> Sherlock still in beta, so it means its not quite ready for production (unless you know what u doing and can handle migrations in a few weeks) </p>
      <p style="margin-left:20px"> If you found any bug, please added them on the github issues... but we also appreciate a PR to fix it :) <p/>
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
      showGreetings: false,
      filterActive: false,
      filterClose: false,
      filterNoCycle: false,
      filter: []
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
    },
    filterClick: function (item) {
      if (this.filter.indexOf(item) > -1) {
        var index = this.filter.indexOf(item)
        this.filter.splice(index, 1)
      } else {
        this.filter.push(item)
      }
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

.project_box{
  min-height: 210px;
}

.filter_state {
  border: solid 1px #333;
  border-radius: 7px;
  padding: 0px 20px;
  line-height: 28px;
  text-transform: none;
}

.filter_state:hover{
    font-weight: 500;
    z-index: -1;
    transform: scale(1);
    box-shadow: 3px 4px 7px -4px #000000;
    -webkit-box-shadow: 3px 4px 7px -4px #000000;
    -moz-box-shadow: 3px 4px 7px -4px #000000;
    box-shadow: 3px 4px 7px -4px #444444;
}

.filter_state_active{
    color: #fff !important;
    background-color: #2f5c86;
    font-weight: 500;
    z-index: -1;
    transform: scale(.9);
    box-shadow: 3px 4px 7px -4px #000000;
    -webkit-box-shadow: 3px 4px 7px -4px #000000;
    -moz-box-shadow: 3px 4px 7px -4px #000000;
    box-shadow: 3px 4px 7px -4px #444444;
}


.animated {
    display: inline-block;
}

.animated.v-enter {
    animation: fadein .5s;
}

.animated.v-leave {
    animation: fadeout .5s;
}

@keyframes fadein {
    0% {
        transform: scale(0);
    }
    50% {
        transform: scale(1.5);
    }
    100% {
        transform: scale(1);
    }
}

@keyframes fadeout {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.5);
    }
    100% {
        transform: scale(0);
    }
}

</style>
