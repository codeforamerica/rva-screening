var DEPENDENCY_PROCESSORS = {
  "equals": function(answer, comparator){
    return answer == comparator;
    },
  "in": function(answer, comparator){
    return $.inArray(answer, comparator) > -1;
  },
  "contains": function(answer, comparator){
    console.log($.inArray(comparator, answer));
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

