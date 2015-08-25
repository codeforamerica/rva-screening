var validations = validations || {};
validations.config = [
  { 
    selector: fName("household_income"), 
    validators: [
      { 
        type: "currency", 
        success: validations.reports.default, 
        failure: validations.reports.failure
      } 
    ]
  },
  { 
    selector: fName("dob"), 
    validators: [
      { 
        type: "required",
        success: validations.reports.default,
        failure: validations.reports.required
      },
      { 
        type: "dob",
        success: validations.reports.success,
        failure: validations.reports.failure
      }  
    ]
  },
  { 
    selector: fName("first_name"),
    validators: [
      { 
        type: "required",
        success: validations.reports.success,
        failure: validations.reports.required
      }
    ]
  },
  {
    selector: fName("ssn"),
    validators: [
      {
        type: "ssn",
        success: validations.reports.success,
        failure: validations.reports.failure
      }
    ]
  }
];

$(function(){
  if ($('.validation').length) {
    V = new Validator('.validation', validations.config);
    validations.bindings.forEach(registerOneWayDataBinding);
    console.info("Registered Validations & Bindings :)");
  }
});