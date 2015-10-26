describe('Validation', function() {

  var v, testValidator;

  var config_dob = [{selector:fName("dob"),validators:[{type:"required",success:reports.default,failure:reports.required},{type:"dob",success:reports.success,failure:reports.failure}]}];
  var config_binding = [{ origin: "dob", recipient:"#dob_recipient", type: "text" }];

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
      expect(res.passed).to.equal(true);
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
      expect(res.passed).to.equal(true);
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
      expect(res.passed).to.equal(false);
    });

    it('phone: fails with improper number length', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'phone',
        name: 'phone_number',
        type: 'text',
        value: '777877'
      }, 'test-form');
      var res = testValidator.validationFunctions['phone']($('#phone'));
      expect(res.passed).to.equal(false);
    });

    it('phone: fails using periods', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'phone',
        name: 'phone_number',
        type: 'text',
        value: '123.123.1234'
      }, 'test-form');
      var res = testValidator.validationFunctions['phone']($('#phone'));
      expect(res.passed).to.equal(false);
    });

    // it('phone: fails with improper parentheses 1', function() {
    //   var testValidator = new v('.validation', []);
    //   createField('input', {
    //     id: 'phone',
    //     name: 'phone_number',
    //     type: 'text',
    //     value: '(123- 456-7890'
    //   }, 'test-form');
    //   var res = testValidator.validationFunctions['phone']($('#phone'));
    //   expect(res.passed).to.equal(false);
    // });

    // it('phone: fails with improper parentheses 2', function() {
    //   var testValidator = new v('.validation', []);
    //   createField('input', {
    //     id: 'phone',
    //     name: 'phone_number',
    //     type: 'text',
    //     value: '123)456-7890'
    //   }, 'test-form');
    //   var res = testValidator.validationFunctions['phone']($('#phone'));
    //   expect(res.passed).to.equal(false);
    // });

    it('phone: passes with no dashes', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'phone',
        name: 'phone_number',
        type: 'text',
        value: '1231231234'
      }, 'test-form');
      var res = testValidator.validationFunctions['phone']($('#phone'));
      expect(res.passed).to.equal(true);
    });

    it('phone: passes with proper dashes', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'phone',
        name: 'phone_number',
        type: 'text',
        value: '123-123-1234'
      }, 'test-form');
      var res = testValidator.validationFunctions['phone']($('#phone'));
      expect(res.passed).to.equal(true);
    });

    it('phone: passes with parentheses and space', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'phone',
        name: 'phone_number',
        type: 'text',
        value: '(123) 123-1234'
      }, 'test-form');
      var res = testValidator.validationFunctions['phone']($('#phone'));
      expect(res.passed).to.equal(true);
    });

    it('phone: passes with parentheses, no space', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'phone',
        name: 'phone_number',
        type: 'text',
        value: '(123)123-1234'
      }, 'test-form');
      var res = testValidator.validationFunctions['phone']($('#phone'));
      expect(res.passed).to.equal(true);
    });

    it('email: fails only domain', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'email',
        name: 'email',
        type: 'email',
        value: 'codeforamerica.org'
      }, 'test-form');
      var res = testValidator.validationFunctions['email']($('#email'));
      expect(res.passed).to.equal(false);
    });

    it('email: fails missing recipient', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'email',
        name: 'email',
        type: 'email',
        value: '@codeforamerica.org'
      }, 'test-form');
      var res = testValidator.validationFunctions['email']($('#email'));
      expect(res.passed).to.equal(false);
    });

    it('email: fails without domain', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'email',
        name: 'email',
        type: 'email',
        value: 'example@codeforamerica'
      }, 'test-form');
      var res = testValidator.validationFunctions['email']($('#email'));
      expect(res.passed).to.equal(false);
    });

    it('email: fails without @', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'email',
        name: 'email',
        type: 'email',
        value: 'examplecodeforamerica.org'
      }, 'test-form');
      var res = testValidator.validationFunctions['email']($('#email'));
      expect(res.passed).to.equal(false);
    });

    it('email: passes with example@codeforamerica.org', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'email',
        name: 'email',
        type: 'email',
        value: 'example@codeforamerica.org'
      }, 'test-form');
      var res = testValidator.validationFunctions['email']($('#email'));
      expect(res.passed).to.equal(true);
    });

    it('zip: passes with 5 digit, 12345', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'zip',
        name: 'zip_code',
        type: 'text',
        value: '12345'
      }, 'test-form');
      var res = testValidator.validationFunctions['zip']($('#zip'));
      expect(res.passed).to.equal(true);
    });

    it('zip: passes with 9 digit, 12345-9876', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'zip',
        name: 'zip_code',
        type: 'text',
        value: '12345-9876'
      }, 'test-form');
      var res = testValidator.validationFunctions['zip']($('#zip'));
      expect(res.passed).to.equal(true);
    });

    it('zip: fails incorrect digits, 1234', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'zip',
        name: 'zip_code',
        type: 'text',
        value: '1234'
      }, 'test-form');
      var res = testValidator.validationFunctions['zip']($('#zip'));
      expect(res.passed).to.equal(false);
    });

    it('zip: fails with dash and no extra digits, 12345-', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'zip',
        name: 'zip_code',
        type: 'text',
        value: '12345-'
      }, 'test-form');
      var res = testValidator.validationFunctions['zip']($('#zip'));
      expect(res.passed).to.equal(false);
    });

    it('zip: fails with no dash, 123459876', function() {
      var testValidator = new v('.validation', []);
      createField('input', {
        id: 'zip',
        name: 'zip_code',
        type: 'text',
        value: '123459876'
      }, 'test-form');
      var res = testValidator.validationFunctions['zip']($('#zip'));
      expect(res.passed).to.equal(false);
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
      var res = testValidator.validationFunctions['dob']($('#dob'));
      expect(res.passed).to.equal(true);
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
      var res = testValidator.validationFunctions['dob']($('#dob'));
      expect(res.passed).to.equal(false);
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
      expect(res.passed).to.equal(true);
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
      expect(res.passed).to.equal(false);
    });
  });

  describe('The Validator', function() {
    // var expectedFields = 
    var newValidator = {selector:fName("family_member_dob"),validators:[{type:"dob",success:reports.success,failure:reports.failure}]};
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

    // // function not in use
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
    it('validated element shows proper valid class after trigger', function() {
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

    it('validated element shows proper invalid class after trigger', function() {
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

    it('validation element with no input length removes validation class', function() {
      var config_ssn = [{selector:fName("ssn"),validators:[{type:"ssn",success:reports.success,failure:reports.failure}]}];
      var testValidator = new v('.validation', config_ssn);
      createField('label', {
        id: 'wrapper',
        class: 'form_field first_name block_4 validation_valid'
      }, 'test-form');
      createField('input', {
        id: 'ssn',
        name: 'ssn',
        type: 'text',
        value: '222-22-2222'
      }, 'wrapper');
      $('#ssn').val('').change();
      $('#ssn').trigger('validation:ssn:success', {});
      expect($('#ssn').parent().hasClass('validation_valid')).to.eq(false);
    });

    it('properly selects multiple inputs if using regex selector', function() {
      var config_multiSelect = [{selector:"[name*=pirate]",validators:[{type:"dob",success:reports.success,failure:reports.failure}]}];
      var testValidator = new v('.validation', config_multiSelect); // selects any field with "pirates" in the name
      // :not([name*=cowboys])

      createField('label', {
        id: 'pirate_wrapper',
        class: 'form_field first_name block_4'
      }, 'test-form');
      createField('input', {
        id: 'pirate_test',
        max: '2200-01-01',
        min: '1899-01-01',
        name: 'pirate_date_of_birth',
        type: 'date',
        value: '1950-06-18'
      }, 'pirate_wrapper');

      createField('label', {
        id: 'pirate_parent_wrapper',
        class: 'form_field first_name block_4'
      }, 'test-form');
      createField('input', {
        id: 'pirate_parent_test',
        max: '2200-01-01',
        min: '1899-01-01',
        name: 'pirate_parent_date_of_birth',
        type: 'date',
        value: '1989-06-18'
      }, 'pirate_parent_wrapper');

      // trigger success dob on both and check if they are valid
      $('#pirate_test').trigger('validation:dob:success', {});
      $('#pirate_parent_test').trigger('validation:dob:success', {});
      expect($('#pirate_parent_wrapper').hasClass('validation_valid')).to.eq(true);
      expect($('#pirate_wrapper').hasClass('validation_valid')).to.eq(true);
    });

    it('properly selects multiple inputs if using exclusion regex selector', function() {
      var config_multiSelect = [{selector:"[name*=pirate]:not([name*=cowboy])",validators:[{type:"dob",success:reports.success,failure:reports.failure}]}];
      var testValidator = new v('.validation', config_multiSelect); // selects any field with "pirates" in the name

      createField('label', {
        id: 'pirate_wrapper',
        class: 'form_field first_name block_4'
      }, 'test-form');
      createField('input', {
        id: 'pirate_test',
        max: '2200-01-01',
        min: '1899-01-01',
        name: 'pirate_date_of_birth',
        type: 'date',
        value: '1950-06-18'
      }, 'pirate_wrapper');

      createField('label', {
        id: 'pirate_parent_wrapper',
        class: 'form_field first_name block_4'
      }, 'test-form');
      createField('input', {
        id: 'pirate_parent_test',
        max: '2200-01-01',
        min: '1899-01-01',
        name: 'pirate_parent_date_of_birth',
        type: 'date',
        value: '1989-06-18'
      }, 'pirate_parent_wrapper');

      createField('label', {
        id: 'pirate_cowboy_wrapper',
        class: 'form_field first_name block_4'
      }, 'test-form');
      createField('input', {
        id: 'pirate_cowboy_test',
        max: '2200-01-01',
        min: '1899-01-01',
        name: 'pirate_cowboy_date_of_birth',
        type: 'date',
        value: '1989-06-18'
      }, 'pirate_cowboy_wrapper');

      // trigger success dob on all three, but assume cowboy doesn't trigger
      $('#pirate_test').trigger('validation:dob:success', {});
      $('#pirate_parent_test').trigger('validation:dob:success', {});
      $('#pirate_cowboy_test').trigger('validation:dob:success', {});
      expect($('#pirate_parent_wrapper').hasClass('validation_valid')).to.eq(true);
      expect($('#pirate_wrapper').hasClass('validation_valid')).to.eq(true);
      expect($('#pirate_cowboy_wrapper').hasClass('validation_valid')).to.eq(false);
    });
  });

  describe('Bindings', function() {
    it('Text processor binds origin to recipient properly', function() {
      var testDateValue = '1914-06-18';
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
        value: testDateValue
      }, 'wrapper');
      createField('p', {
        id: 'dob_recipient'
      }, 'wrapper');
      config_binding.forEach(registerOneWayDataBinding);
      $('#test-field').trigger('change');
      expect($('#dob_recipient').text()).to.equal(testDateValue);
    });
  });

  describe('Dirty form check', function() {
    it('sets dirty option to true, and adds class', function() {
      var testValidator = new v('.validation', config_dob);
      testValidator.dirt();
      expect(testValidator.dirty).to.equal(true);
      expect($('form').hasClass('validation_dirty')).to.equal(true);
    });
  });

});