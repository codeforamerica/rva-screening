var validations = validations || {};
validations.reports = {
  "default": function(e, result) {
    console.log(e.type, arguments);
  },
  "failure": function(e, result) {
    console.log(e.type, arguments);
    console.error(result.message);
    validationHTML(arguments[0].currentTarget, 'validation_invalid');
  },
  "success": function(e, result) {
    console.log(e.type, arguments);
    validationHTML(arguments[0].currentTarget, 'validation_valid');
  },
  "required": function(e, result) {
    console.log(e.type, arguments);
    validationHTML(arguments[0].currentTarget, 'validation_required');
  }
}