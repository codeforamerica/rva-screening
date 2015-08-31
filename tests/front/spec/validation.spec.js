describe('Validation', function() {

  var v, testValidator;

  var config_dob = [{selector:fName("dob"),validators:[{type:"required",success:validations.reports.default,failure:validations.reports.required},{type:"dob",success:validations.reports.success,failure:validations.reports.failure}]}];

  // TODO: make these less brittle - currently depend on message string matching with deep.equal()
  var expectedResponses = {
    dob_true: {passed: true, value: 19140618, message: 'Something may have gone wrong but it could have gone right.'},
    dob_false: {passed: false, value: 'waka', message: 'It looks like you\'ve entered an incorrect currency amount.'},
    required_true: {passed: true, value: 'some required text', message: 'Something may have gone wrong but it could have gone right.'},
    required_false: {passed: false, value: '', message: 'This field is required!'},
    ssn_true: {passed: true, value: '222-22-2222', message: 'Something may have gone wrong but it could have gone right.'},
    ssn_false: {passed: false, value: '222-22-222', message: 'Not a valid social security number.'},
    currency_true: {passed: true, value: 300, message: 'Something may have gone wrong but it could have gone right.'},
    currency_false: {passed: false, value: '', message: 'It looks like you\'ve entered an incorrect currency amount.'}
  };

  function createField(type, attributes, parentId) {
    var elem = document.createElement(type);
    for (a in attributes) {
      elem.setAttribute(a, attributes[a]);
    }
    document.getElementById(parentId).appendChild(elem);
    // <input class="field_input" id="dob" max="2200-01-01" min="1899-01-01" name="dob" type="date" value="1914-06-18">
  };

  function createForm(className, id) {
    var form = document.createElement('form');
    form.className = className;
    form.id = id;
    document.body.appendChild(form);
  }

  beforeEach(function() {
    createForm('validation', 'test-form');
    v = Validator; // locally scoped Validator
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  describe('Initialization', function() {
    it('throws error if root element does not exist', function() {
      $('#test-form').removeClass('validation').addClass('another-class');
      expect(function() { new v('.validation', []); }).to.throw(Error);
    });

    it('throws error if config is not properly set or formatted', function() {
      // TODO: write config validator in validation.js
    });
  });

  describe('validator functions', function() {

    it('able to access validator functions', function() {
      var testValidator = new v('.validation', []);
      expect(Object.keys(testValidator.validationFunctions).length).to.not.equal(0);
    });
    
    it('currency: proper input returns true validation result', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'income',
        name: 'make-money-get-paid',
        type: 'number',
        value: '300'
      }, 'test-form');
      var res = testValidator.validationFunctions['currency']($('#income'));
      expect(res).to.deep.equal(expectedResponses.currency_true);
    });

    it('currency: improper input returns false validation result', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'income',
        name: 'make-money-get-paid',
        type: 'number',
        value: '3o0'
      }, 'test-form');
      var res = testValidator.validationFunctions['currency']($('#income'));
      expect(res).to.deep.equal(expectedResponses.currency_false);
    });

    it('ssn: proper input returns true validation result', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'ssn',
        name: 'ssn',
        type: 'text',
        value: '222-22-2222'
      }, 'test-form');
      var res = testValidator.validationFunctions['ssn']($('#ssn'));
      expect(res).to.deep.equal(expectedResponses.ssn_true);
    });

    it('ssn: improper input returns false validation result', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'ssn',
        name: 'ssn',
        type: 'text',
        value: '222-22-222'
      }, 'test-form');
      var res = testValidator.validationFunctions['ssn']($('#ssn'));
      expect(res).to.deep.equal(expectedResponses.ssn_false);
    });

    it('dob: proper input returns true validation result', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'dob',
        max: '2200-01-01',
        min: '1899-01-01',
        name: 'dob',
        type: 'date',
        value: '1914-06-18'
      }, 'test-form');
      var res = testValidator.validationFunctions['currency']($('#dob'));
      expect(res).to.deep.equal(expectedResponses.dob_true);
    });

    it('dob: improper input returns false validation result', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'dob',
        max: '2200-01-01',
        min: '1899-01-01',
        name: 'dob',
        type: 'date',
        value: 'waka'
      }, 'test-form');
      var res = testValidator.validationFunctions['currency']($('#dob'));
      expect(res).to.deep.equal(expectedResponses.dob_false);
    });

    it('required: proper input returns true validation result', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'something-required',
        name: 'a-required-field',
        type: 'text',
        value: 'some required text'
      }, 'test-form');
      var res = testValidator.validationFunctions['required']($('#something-required'));
      expect(res).to.deep.equal(expectedResponses.required_true);
    });

    it('required: improper input returns false validation result', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'something-required',
        name: 'a-required-field',
        type: 'text',
        value: ''
      }, 'test-form');
      var res = testValidator.validationFunctions['required']($('#something-required'));
      expect(res).to.deep.equal(expectedResponses.required_false);
    });
  });

  describe('The Validator', function() {
    // var expectedFields = 
    var newValidator = {selector:fName("family_member_dob"),validators:[{type:"dob",success:validations.reports.success,failure:validations.reports.failure}]}
    var testFieldName = 'waka';
    var expectedFieldNameResponse = '[name=\'waka\']';
    it('fName() structures properly', function() {
      expect(fName(testFieldName)).to.eq(expectedFieldNameResponse);
    });

    it('properly adds a new validation function, using Validator.addValidationFn', function() {
      var testValidator = new v('.validation', []);
      var newValidationFunction = function(string) {
        return string + 'flaka';
      };
      var beforeAddition = testValidator.validationFunctions;
      var afterAddtion = testValidator.addValidationFn('newValidationFunction', newValidationFunction);
      expect(beforeAddition).to.not.deep.equal(afterAddtion);

      var res = testValidator.validationFunctions.newValidationFunction('waka');
      expect(res).to.equal('wakaflaka');
    });

    // it('properly adds a new validator using Validator.addValidator', function() {
    //   var newValidator = function(x) {
    //     return x + 1
    //   };
    //   testValidator.addValidator('dob', newValidator);
    //   console.log()
    // });

    it('adds validation classes as expected', function() {
      createField('label', {
        id: 'wrapper',
        class: 'form_field first_name block_4'
      }, 'test-form');
      createField('input', {
        id: 'test-field'
      }, 'wrapper');
      validationHTML('#test-field', 'validation_class');
      expect($('#test-field').parent().hasClass('validation_class')).to.eq(true);
    });


    it('removes validation classNames successfully from parent using removeValidationClasses()', function() {
      createField('label', {
        id: 'wrapper',
        class: 'form_field first_name block_4 validation_valid'
      }, 'test-form');
      createField('input', {
        id: 'test-field'
      }, 'wrapper');
      removeValidationClasses($('#test-field'));
      expect($('#test-field').parent().hasClass('validation_valid')).to.eq(false);
    });
  });

  describe('Triggers', function() {
    it('validated element shows proper validation class after trigger', function() {
      var testValidator = new v('.validation', config_dob);
      createField('label', {
        id: 'wrapper',
        class: 'form_field first_name block_4'
      }, 'test-form');
      createField('input', {
        id: 'test-field',
        max: '2200-01-01',
        min: '1899-01-01',
        name: 'dob',
        type: 'date',
        value: '1914-06-18'
      }, 'wrapper');
      $('#test-field').trigger('validation:dob:success', {});
      expect($('#test-field').parent().hasClass('validation_valid')).to.eq(true);
    });

    it('validated element shows proper validation class after trigger', function() {
      var testValidator = new v('.validation', config_dob);
      createField('label', {
        id: 'wrapper',
        class: 'form_field first_name block_4'
      }, 'test-form');
      createField('input', {
        id: 'test-field',
        max: '2200-01-01',
        min: '1899-01-01',
        name: 'dob',
        type: 'date',
        value: '1899-06-18' //invalid date
      }, 'wrapper');
      $('#test-field').trigger('validation:dob:failure', {});
      expect($('#test-field').parent().hasClass('validation_invalid')).to.eq(true);
    });
  });

});