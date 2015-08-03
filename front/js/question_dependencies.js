var EMPLOYED = [ "FT", "PT", "SEA" ];

var DEPENDENCIES = [
  { target: "marital_status", child: "spouse_employment_status", 
    type: "equals", comparator: "MAR" },
  { target: "spouse_employment_status", child: "spouse_years_at_current_employer ", 
    type: "in", comparator: EMPLOYED },
  { target: "employment_status", child: "employers",
    type: "in", comparator: EMPLOYED },
  { target: "employment_status", child: "years_at_current_employer ",
    type: "in", comparator: EMPLOYED },
  { target: "spouse_employment_status", child: "spouse_years_at_current_employer",
    type: "in", comparator: EMPLOYED },
  { target: "employment_status", child: "time_unemployed",
    type: "equals", comparator: "UNE" },
  { target: "spouse_employment_status", child: "spouse_time_unemployed",
    type: "equals", comparator: "UNE" },
  { target: "insurance_status", child: "coverage_type",
    type: "equals", comparator: "Y" },

  { target: "veteran_yn", child: "applied_for_vets_benefits_yn",
    type: "equals", comparator: "Y" },
  { target: "eligible_for_vets_benefits_yn", child: "applied_for_vets_benefits_yn",
    type: "equals", comparator: "Y" },

  { target: "applied_for_medicaid_yn", child: "medicaid_date_effective",
    type: "equals", comparator: "Y" },
  { target: "applied_for_ssd_yn", child: "ssd_date_effective",
    type: "equals", comparator: "Y" },
  { target: "are_due_to_accident", child: "accident_work_related_yn",
    type: "equals", comparator: "Y" },

  { target: "race", child: "race_other",
    type: "equals", comparator: "OTH" },
  { target: "languages", child: "languages_other",
    type: "contains", comparator: "OTH" },
  { target: "housing_status", child: "housing_status_other",
    type: "equals", comparator: "OTH" },
  { target: "coverage_type", child: "coverage_type_other",
    type: "equals", comparator: "OTH" },

  { target: "languages", child: "has_interpreter_yn",
    type: "does_not_contain", comparator: "EN" },
];

var DEPENDENCY_PROCESSORS = {
  "equals": function(answer, comparator){
    return answer == comparator;
    },
  "in": function(answer, comparator){
    return $.inArray(answer, comparator) > -1;
  },
  "contains": function(answer, comparator){
    return $.inArray(comparator, answer) > -1;
  },
  "does_not_contain": function(answer, comparator){
    return $.inArray(comparator, answer) == -1;
  },
};

function registerConditionalDisplay(d){
  // parse the dependency and get elements
  var target = $("."+d.target+" [name='"+d.target+"']");
  var child = $("."+d.child);
  var processor = DEPENDENCY_PROCESSORS[d.type];
  var comparator = d.comparator;
  // make a function to hide or show the child element
  var displayFunction = function(){
    // console.log("parent:", target[0], "child:", child[0]);
    // console.log("changed to", target.val());
    // console.log("met criteria:", processor(target.val(), comparator));
    if( processor(target.val(), comparator) ){
      child.show();
    } else {
      child.hide();
    };
  }
  // set the event listener to trigger the function
  target.on("change", function(e){ displayFunction(); });
  // trigger the function
  displayFunction();
}

$(function(){
  DEPENDENCIES.forEach(registerConditionalDisplay);
  console.info("Registered Dependencies :)");
});

