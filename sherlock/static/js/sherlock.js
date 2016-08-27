function show_tst_case(scenario_id, url_){
  show_tst_case_icons(scenario_id);
  $.ajax({
          url: url_,
          type: 'GET',
          success: function(response) {
              $( ".cases_col" ).empty();
              var cases = response[0].reverse();
              cases.forEach( function (arrayItem){
                mount_tst_box(arrayItem)
              });
          },
          error: function(error) {
              console.log(error);
          }
        });
}



$('#editScenario').on('show.bs.modal', function(e) {
    var scenario_id = $(e.relatedTarget).data('scenario-id');
    var scenario_name = $(e.relatedTarget).data('scenario-name');

    //populate the textbox
    $(e.currentTarget).find('input[id="input_edit_scenario_name"]').val(scenario_name);
    $(e.currentTarget).find('input[id="edited_scenario_id"]').val(scenario_id);
});

$('#editTstcase').on('show.bs.modal', function(e) {
    var case_id = $(e.relatedTarget).data('case-id');
    var case_name = $(e.relatedTarget).data('case-name');
    var scenario_case_id = $(e.relatedTarget).data('scenario-case-id');

    //populate the textbox
    $(e.currentTarget).find('input[id="input_edit_case_name"]').val(case_name);
    $(e.currentTarget).find('input[id="edited_case_id"]').val(case_id);
    $(e.currentTarget).find('input[id="edited_case_scenario_id"]').val(scenario_case_id);
});

function edit_scenario() {

  var edited_scenario_id = $('#edited_scenario_id').val();
  var csrftoken = $('meta[name=csrf-token]').attr('content')
  var scenario_name = $('#input_edit_scenario_name').val();
  var scenario_id = $('#edited_scenario_id').val();
  var url_ = '../edit/'.concat(edited_scenario_id)
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
              if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken)
          }
        }
        })
        $.ajax({
            url: url_,
            data: JSON.stringify({scenario_name: scenario_name, csrftoken: csrftoken}),
            type: 'POST',
            contentType:"application/json",
            dataType:"json",
            success: function(response) {
              if (response.status === "ok"){
                $('#editScenario').modal('hide');
                $('#tst_scenario_'+response.scenario_id+'_value').empty();
                $('#tst_scenario_'+response.scenario_id+'_value').html(response.scenario_name);
              }
            },
            error: function(error) {
                console.log(error);
            },
        });
}

function edit_case() {

  var edited_case_id = $('#edited_case_id').val();
  var csrftoken = $('meta[name=csrf-token]').attr('content')
  var case_name = $('#input_edit_case_name').val();
  var scenario_id = $('#edited_case_scenario_id').val();
  var url_ = '/scenario/'.concat(scenario_id,'/tst_case/edit/', edited_case_id)

  var scenario_id = $('#edited_scenario_id').val();
          $.ajaxSetup({
            beforeSend: function(xhr, settings) {
              if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken)
          }
        }
        })
        $.ajax({
            url: url_,
            data: JSON.stringify({case_name: case_name, csrftoken: csrftoken}),
            type: 'POST',
            contentType:"application/json",
            dataType:"json",
            success: function(response) {
              if (response.status === "ok"){
                $('#editTstcase').modal('hide');
                $('#tst_case_'+response.case_id+'_value').empty();
                $('#tst_case_'+response.case_id+'_value').html(response.case_name);
              }
            },
            error: function(error) {
                console.log(error);
            },
        });
}

/* COMMOM OPERATIONS */


function mount_tst_box(arrayItem){
  $(".cases_col").append($("<div/>",{"id": "tst_case_row_"+arrayItem.id, "class":"row display_item_box"}));
  $("#tst_case_row_"+arrayItem.id).append($("<div/>",{"id": "tst_case_"+arrayItem.id+"_value", "class":"col-md-11"}));
  $("#tst_case_row_"+arrayItem.id).append($("<div/>",{"id": "tst_case_"+arrayItem.id+"_edit", "class":"col-md-1"}));
  $("#tst_case_"+arrayItem.id+"_value").html(arrayItem.name);
  $("#tst_case_"+arrayItem.id+"_edit").html("<a data-toggle='modal' data-target='#editTstcase'" +
        "data-case-id='"+ arrayItem.id+"' data-case-name='"+ arrayItem.name+"', data-scenario-case-id='"+arrayItem.scenario_id+"'>" +
        "<i class='fa fa-pencil-square-o fa-2x' aria-hidden='true'></i> </a>");
}

function concat_name(hash, item_name, id){
  return hash.concat(item_name,id)
}

function add_class_current() {
  for (var i = 0; i < arguments.length; i++) {
    $(arguments[i]).addClass("current");
  }
}

function show_tst_case_icons(scenario_id){
  var tst_scenario = concat_name("#","tst_scenario_",scenario_id);
  var show_icon = concat_name("#","show_icon_",scenario_id);
  var edit_icon = concat_name("#","current_test_scenario_",scenario_id);

  $('.scenarios_col').find('.current').removeClass('current');
  $('.scenarios_col').find('.show').removeClass('show');

  add_class_current(tst_scenario,show_icon, edit_icon);
  $(edit_icon).addClass("show");
}



/* CYCLES */

function change_case_status_for_cycle_history(case_id, state_code, cycle_id) {

  var csrftoken = $('meta[name=csrf-token]').attr('content')
  var url_ = '../edit/' + cycle_id
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
              if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken)
          }
        }
        })
        $.ajax({
            url: url_,
            data: JSON.stringify({case_id: case_id, state_code: state_code, csrftoken: csrftoken}),
            type: 'POST',
            contentType:"application/json",
            dataType:"json",
            success: function(response) {
              if (response.status === "ok"){
                $('#PASSED_case_id_'+response.case_id).removeClass( "PASSED" )
                $('#ERROR_case_id_'+response.case_id).removeClass( "ERROR" )
                $('#BLOCKED_case_id_'+response.case_id).removeClass( "BLOCKED" )

                if(response.state_code === "PASSED"){
                  $('#PASSED_case_id_'+case_id).addClass( "PASSED" )
                }
                if(response.state_code === "ERROR"){
                  $('#ERROR_case_id_'+case_id).addClass( "ERROR" )
                }
                if(response.state_code === "BLOCKED"){
                  $('#BLOCKED_case_id_'+case_id).addClass( "BLOCKED" )
                }
                
                reload_cycle_total_count(cycle_id)

              }
            },
            error: function(error) {
                console.log(error);
            },
        });
}

function reload_cycle_total_count(cycle_id){
  _url = '../get_states/' + cycle_id
  $.ajax({
          url: _url,
          type: 'GET',
          success: function(response) {
              $( "#show_total_not_executed" ).empty();
              $( "#show_total_passed" ).empty();
              $( "#show_total_notpassed" ).empty();
              $( "#show_total_blocekd" ).empty();

              $('#show_total_not_executed').html(response.total_not_executed);
              $('#show_total_passed').html(response.total_passed);
              $('#show_total_error').html(response.total_error);
              $('#show_total_blocked').html(response.total_blocked);
          },
          error: function(error) {
              console.log(error);
          }
        });

}
