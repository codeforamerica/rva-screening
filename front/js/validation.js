function validationResult(res, val){
  return { passed: res, value: val };
}

var DEFAULT_VALIDATORS = {
  "currency": function ($elem) {
    var val = $elem.val();
    // parse as currency - via http://stackoverflow.com/a/559178/399726
    var cleaned = val.replace(/[^0-9\.]+/g,"");
    var parsed = Math.round( parseFloat(cleaned));
    if( isNaN(parsed) ){
      return validationResult(false, val);
    } else {
      return validationResult(true, parsed);
    }
  },
  "required": function ($elem) {
    // fails on falsey values
    var val = $elem.val();
    if( val ){
      return validationResult(true, val);
    } else {
      return validationResult(false, val);
    }
  },
  "date": function ($elem) {
    // attempts default javascript date parsing
    var val = $elem.val();
    var parsed = new Date(val);
    if( isNaN(parsed) ){
      return validationResult(false, val);
    } else {
      return validationResult(true, parsed);
    }
  },
  "dob": function ($elem) {
    console.log(this);
    var val = $elem.val();
    var parsed = new Date(val);
    if( isNaN(parsed) ){
      return validationResult(false, val);
    } else {
      return validationResult(true, parsed);
    }
  }
};

 

function Validator(root, fields, validationFunctions){
  this.validateOn = 'change';
  this.$root = $(root);
  this.validationFunctions = validationFunctions || DEFAULT_VALIDATORS;
  this.fields = fields || [];
  this.init();
}

Validator.prototype = {

  VALIDATION_EVENT_TYPES: ['complete', 'failure', 'success'],

  createListener: function(validators){
    var V = this;
    return function(e){
      var allPassed = false;
      var target = $(this);

      var results = validators.map(function(v){
        var result = V.validationFunctions[v.type](target);
        var typeScope = 'validation:' + v.type + ':';
        result.validator = v.type;
        if( result.passed ){
          target.trigger(typeScope + 'success', [result]);
        } else {
          target.trigger(typeScope + 'failure', [result]);
        }
        target.trigger(typeScope + 'complete', [result]);
        allPassed = allPassed && result.passed;
        return result;
      });

      if( allPassed ){
        target.trigger("validation:success", results);
      } else {
        target.trigger("validation:failure", results);
      }
      target.trigger("validation:complete", results);
    };
  },

  addValidator: function addValidator(key, fn){
    this.validators[key] = fn;
  },

  listenToField: function listenToField(selector, validators, eventType){
    var V = this;
    this.fields.push({ 'selector': selector, 
      'validators': validators });

    // bind callbacks to validation events, using delegation
    validators.forEach(function(v){
      V.VALIDATION_EVENT_TYPES.forEach(function(eventType){
        if( v[eventType] ){
          V.$root.on( 'validation:'+v.type+':'+eventType,
            selector, v[eventType] );
        }
      });
    });

    // create main listener with Assigned 
    // validation functions and triggers
    this.$root.on( eventType || this.validateOn, selector, 
        this.createListener(validators) );
  },

  init: function init(){
    var V = this;
    this.fields.forEach(function(f){
      V.listenToField(f.selector, f.validators);
    });
    var listeners = $._data(V.$root[0], "events");
  }

};


// handle validation messages and values
var reports = {
  "default": function(e, result) {
    console.log(e.type, arguments);
  },
  "dobFailure": function(e, result) {
    alert('please enter a date prior to today.');
  },
  "incomeFailure": function(e, result){
    alert("please enter a whole dollar amount.");
  }
}

function fName(s){
  return "[name='"+s+"']";
}
var validations = [
  { 
    selector: fName("household_income"), 
    validators: [
      { 
        type: "currency", 
        success: reports.default, 
        failure: reports.incomeFailure
      } 
    ]
  },
  { 
    selector: fName("dob"), 
    validators: [
      { 
        type: "required",
        success: reports.default,
        failure: reports.default
      },
      { 
        type: "dob",
        success: reports.default,
        failure: reports.dobFailure
      }  
    ]
  },
  { 
    selector: fName("first_name"),
    validators: [
      { 
        type: "required",
        success: reports.default,
        failure: reports.default
      }
    ]
  },
];