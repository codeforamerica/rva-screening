var validations = validations || {};
function validationResult(res, val, message){
  return { passed: res, value: val, message: message || 'Something may have gone wrong but it could have gone right.' };
}

var DEFAULT_VALIDATORS = {
  "currency": function ($elem) {
    var val = $elem.val();
    // parse as currency - via http://stackoverflow.com/a/559178/399726
    var cleaned = val.replace(/[^0-9\.]+/g,"");
    var parsed = Math.round( parseFloat(cleaned));
    if( isNaN(parsed) ){
      return validationResult(false, val, 'It looks like you\'ve entered an incorrect currency amount.');
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
      return validationResult(false, val, 'This field is required!');
    }
  },
  "date": function ($elem) {
    // attempts default javascript date parsing
    var val = $elem.val();
    var parsed = new Date(val);
    var nextYear = new Date(new Date().setYear(new Date().getFullYear() + 1))
    var nextYearNice = nextYear.getMonth() + '/' + nextYear.getDate() + '/' + nextYear.getFullYear();
    if( isNaN(parsed) ){
      return validationResult(false, val, 'This is not a valid date.');
    } else if ( parsed > nextYear ) {
      // Allow entering dates up to a year in the future because users sometimes want to 
      // enter future Medicaid effective dates etc
      return validationResult(false, val, 'Please enter a date before ' + nextYearNice);
    } else if ( parsed < new Date(1900, 1, 1) ) {
      return validationResult(false, val, 'Please enter date after 1/1/1900');
    } else {
      return validationResult(true, parsed);
    }
  },
  "dob": function ($elem) {
    // checks date to be before today and after 1900 (currently only checking year)
    var val = $elem.val();
    var parsed = new Date(val);
    var today = new Date();
    var todayNice = today.getMonth() + '/' + today.getDate() + '/' + today.getFullYear();
    if( isNaN(parsed) ){
      return validationResult(false, val, 'This is not a valid date.');
    } else if ( parsed > today ) {
      return validationResult(false, val, 'Please enter a date before ' + todayNice);
    } else if ( parsed < new Date(1900, 1, 1) ) {
      return validationResult(false, val, 'Please enter date after 1/1/1900');
    } else {
      return validationResult(true, parsed);
    }
  },
  "ssn": function($elem) {
    // matches a regex against the value
    var val = $elem.val();
    if(val==='') {
      return validationResult(true, val);
    }
    var pattern = /^\d{3}-?\d{2}-?\d{4}$/;
    if (!val.match(pattern)) {
      return validationResult(false, val, 'Not a valid social security number.');
    } else {
      return validationResult(true, val);
    }
  },
  "phone": function($elem) {
    var val = $elem.val();
    if(val==='') {
      return validationResult(true, val);
    }
    // modified from http://stackoverflow.com/a/7288047
    var pattern = /^[(]{0,1}[0-9]{3}[)]{0,1}[-\s]{0,1}[0-9]{3}[-\s]{0,1}[0-9]{4}$/;
    if (!val.match(pattern)) {
      return validationResult(false, val, 'Not a valid phone number!');
    } else {
      return validationResult(true, val);
    }
  },
  "email": function($elem) {
    var val = $elem.val();
    // http://stackoverflow.com/a/46181
    var pattern = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    if (!val.match(pattern)) {
      return validationResult(false, val, 'Not a valid email address!');
    } else {
      return validationResult(true, val);
    }
  },
  "zip": function($elem) {
    var val = $elem.val();
    if(val==='') {
      return validationResult(true, val);
    }
    http://stackoverflow.com/a/160583
    var pattern = /(^\d{5}$)|(^\d{5}-\d{4}$)/;
    if(!val.match(pattern)) {
      return validationResult(false, val, 'Not a valid postal code!');
    } else {
      return validationResult(true, val);
    }
  }
};


var Validator = function(root, fields, validationFunctions){
  this.validateOn = 'blur';
  if(!$(root)) {
    var err = new Error(root + 'does not exist');
    throw err;
  }
  this.$root = $(root);
  this.validationFunctions = validationFunctions || DEFAULT_VALIDATORS;
  this.fields = fields || [];
  this.init();
  this.dirty = false;
}

Validator.prototype = {

  VALIDATION_EVENT_TYPES: ['complete', 'failure', 'success', 'clear'],

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
        } else if (result.passed === 'clear') {
          console.log(target);
          target.trigger(typeScope + 'clear', [result]);
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

  addValidator: function(key, fn){
    this.validators[key] = fn;
  },

  addValidationFn: function(key, fn){
    this.validationFunctions[key] = fn;
  },

  listenToField: function(selector, validators, eventType){
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
    this.changeDetection();
  },

  changeDetection: function() {
    var V = this;
    var prx = this.proxy(V.dirt, V);

    // detect any changes in the form, pass with proper scope using $.proxy()
    $('.validation :input').on('change', prx);

    $(window).on('beforeunload', function(event) {
      var e = event.originalEvent;
      var confirmationMessage = 'There are unsaved edits on this page. Please save before continuing.';

      // if the form isn't dirty, or if the user is clicking the save button
      if (!V.dirty || e.target.activeElement.getAttribute('type') === 'submit') {
          return undefined;
      }

      (e || window.event).returnValue = confirmationMessage; //Gecko + IE
      return confirmationMessage;
    });
  },

  // only available so we can test
  proxy: function(fn, context) {
    return $.proxy(fn, context);
  },

  dirt: function() {
    this.$root.addClass('validation_dirty');
    this.dirty = true;
    $('#patient_details_form_save').removeClass('button_green_presave').addClass('button_green').text('Save changes');
  }


};

// Removes all instances of classes with 'validation'.
// Used when updating HTML validation
function removeValidationClasses($elem) {
  var $parent = $elem.parent();
  var classList = $parent.attr('class').split(/\s+/);
  $.each( classList, function(index, item){
    if (item.indexOf('validation') > -1) {
      // remove all validation classnames before adding new ones
      $parent.removeClass(item);
    }
  });
}

// Handle validation on the HTML side of things
function validationHTML(elem, className, message) {
  var $input = $(elem);
  removeValidationClasses($input);
  if($input.val().length === 0 && className === 'validation_valid') {
    // if valid but no input, it means the user has removed this information
  } else {
    $input.parent().addClass(className);
    if (message) {
      console.log(message);
      // do this
    }
  }
}

function fName(s){
  return "[name='"+s+"']";
}

reports = {
  "default": function(e, result) {
    // console.log(e.type, arguments);
  },
  "failure": function(e, result) {
    // console.log(e.type, arguments);
    // console.error(result.message); 
    validationHTML(arguments[0].currentTarget, 'validation_invalid');
  },
  "success": function(e, result) {
    // console.log(e.type, arguments);
    validationHTML(arguments[0].currentTarget, 'validation_valid');
  },
  "required": function(e, result) {
    // console.log(e.type, arguments);
    validationHTML(arguments[0].currentTarget, 'validation_required');
  }
}