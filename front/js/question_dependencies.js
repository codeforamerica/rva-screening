








var DEPENDENCIES = [
  { target: "marital_status", child: "spouse_employment_status", 
    type: "equals", comparator: "MAR" },
  { target: "employment_status", child: "employers",
    type: "in", comparator: [ "FT", "PT", "SEA" ] },
  { target: "insurance_status", child: "coverage_type",
    type: "equals", comparator: "Y" },
];

var DEPENDENCY_PROCESSORS = {
  "equals": function(answer, comparator){
    return answer == comparator;
    },
  "in": function(answer, comparator){
    return $.inArray(answer, comparator) > -1;
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
    console.log("parent:", target[0], "child:", child[0]);
    console.log("changed to", target.val());
    console.log("met criteria:", processor(target.val(), comparator));
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
  console.log("registered dependencies");
});

