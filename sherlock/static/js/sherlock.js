function show_tst_case(scenario_id){
  show_tst_case_icons(scenario_id);

  var url_ = '../get_cases_for_scenario/'.concat(scenario_id)
  $.ajax({
          url: url_,
          type: 'GET',
          success: function(response) {
              $( ".cases_col" ).empty();
              cases = response[0].reverse();
              cases.forEach( function (arrayItem){
                $(".cases_col").append(mount_item_box(arrayItem.name));
              });
          },
          error: function(error) {
              $(".cases_col").append(mount_item_box(error));
          }
        });
}



$('#editScenario').on('show.bs.modal', function(e) {
    var scenario_id = $(e.relatedTarget).data('scenario-id');
    var scenario_name = $(e.relatedTarget).data('scenario-name');

    //populate the textbox
    $(e.currentTarget).find('input[id="input_edit_scenario_name"]').val(scenario_name);
});

/* COMMOM OPERATIONS */


function mount_item_box(text){
  return $("<div/>",{"text":text,"class":"display_item_box"});
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
