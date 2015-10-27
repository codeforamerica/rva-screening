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
  "checked": function(answer, comparator) {
    return answer.indexOf(comparator) > -1;
  }
};

function registerConditionalDisplay(d){
  // if the dependency exists within a many-to-one relationship
  if(d.manyToOne) {
    var completeBool = true;
    var completeCount = 0;
    while (completeBool) {
      tempTarget = d.target.replace('X', completeCount);
      tempChild = d.child.replace('X', completeCount);
      if (!$('#'+tempTarget).length) {
        completeBool = false;
      } else {
        setDisplay(tempTarget, tempChild, d.type, d.comparator);
      }
      completeCount++;
    }
  // otherwise parse the single dependency and get elements
  } else {
    setDisplay(d.target, d.child, d.type, d.comparator);
  }
}

function setDisplay(target, child, type, comparator) {
  var $target = $("."+target+" [name='"+target+"']");
  var $child = $("."+child);
  var processor = DEPENDENCY_PROCESSORS[type];
  var comp = comparator;
  // make a function to hide or show the child element
  var displayFunction = function(){
    // console.log("parent:", target[0], "child:", child[0]);
    // console.log("changed to", target.val());
    // console.log("met criteria:", processor(target.val(), comparator));

    var targetVal;
    if (type !== 'checked') {
      targetVal = $target.val();
    } else {
      targetVal = '';
      $target.each(function() {
        if ($(this).is(':checked')) targetVal += $(this).val();
      });
      console.log(targetVal);
    }

    if( processor(targetVal, comp) ){
      $child.show();
    } else {
      $child.hide();
    };
  }
  // set the event listener to trigger the function
  $target.on("change", function(e){ displayFunction(); });
  // trigger the function
  displayFunction();
}