describe('Question Dependencies', function() {

  var exampleEquals = [{ target: "question_a", child: "question_b", type: "equals", comparator: "YES" }];
  var exampleIn = [{ target: "question_a", child: "question_b ", type: "in", comparator: ['ONE', 'TWO', 'THREE'] }];
  var exampleContains = [{ target: "question_a", child: "question_b", type: "contains", comparator: "OTH" }];
  var exampleDoesNotContain = [{ target: "question_a", child: "question_b", type: "does_not_contain", comparator: "WAKA" }];

  beforeEach(function() {
    var div = document.createElement('div');
    div.id = 'wrapper';
    document.body.appendChild(div);
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  describe('Processors', function() {
    it('[equals]: display:none before change', function() {
      createField('label', {
        id: 'question_label',
        class: 'question_a'
      }, 'wrapper');

      createField('input', {
        id: 'question_a',
        name: 'question_a',
        type: 'text',
        value: 'NO'
      }, 'question_label');

      createField('input', {
        id: 'question_b',
        class: 'question_b',
        type: 'text'
      }, 'wrapper');
      exampleEquals.forEach(registerConditionalDisplay);
      var display = $('#question_b').css('display');
      expect(display).to.equal('none');
    });

    it('[equals]: display:none after false change', function() {
      createField('label', {
        id: 'question_label',
        class: 'question_a'
      }, 'wrapper');

      createField('input', {
        id: 'question_a',
        name: 'question_a',
        type: 'text',
        value: 'NO'
      }, 'question_label');

      createField('input', {
        id: 'question_b',
        class: 'question_b',
        type: 'text'
      }, 'wrapper');
      exampleEquals.forEach(registerConditionalDisplay);
      $('#question_a').val('MAYBE').trigger('change');
      var display = $('#question_b').css('display');
      expect(display).to.equal('none');
    });

    it('[equals]: display:inline-block after change', function() {
      createField('label', {
        id: 'question_label',
        class: 'question_a'
      }, 'wrapper');

      createField('input', {
        id: 'question_a',
        name: 'question_a',
        type: 'text',
        value: 'NO'
      }, 'question_label');

      createField('input', {
        id: 'question_b',
        class: 'question_b',
        type: 'text'
      }, 'wrapper');
      exampleEquals.forEach(registerConditionalDisplay);
      $('#question_a').val('YES').trigger('change');
      var display = $('#question_b').css('display');
      expect(display).to.equal('inline-block');
    });

    it('[in]: display:none before change', function() {
      createField('label', {
        id: 'question_label',
        class: 'question_a'
      }, 'wrapper');

      createField('input', {
        id: 'question_a',
        name: 'question_a',
        type: 'text',
        value: 'NUMBER'
      }, 'question_label');

      createField('input', {
        id: 'question_b',
        class: 'question_b',
        type: 'text'
      }, 'wrapper');
      exampleIn.forEach(registerConditionalDisplay);
      var display = $('#question_b').css('display');
      expect(display).to.equal('none');
    });

    it('[in]: display:none after false change', function() {
      createField('label', {
        id: 'question_label',
        class: 'question_a'
      }, 'wrapper');

      createField('input', {
        id: 'question_a',
        name: 'question_a',
        type: 'text',
        value: 'NO'
      }, 'question_label');

      createField('input', {
        id: 'question_b',
        class: 'question_b',
        type: 'text'
      }, 'wrapper');
      exampleIn.forEach(registerConditionalDisplay);
      $('#question_a').val('FOUR').trigger('change');
      var display = $('#question_b').css('display');
      expect(display).to.equal('none');
    });

    it('[in]: display:inline-block after change', function() {
      createField('label', {
        id: 'question_label',
        class: 'question_a'
      }, 'wrapper');

      createField('input', {
        id: 'question_a',
        name: 'question_a',
        type: 'text',
        value: 'NO'
      }, 'question_label');

      createField('input', {
        id: 'question_b',
        class: 'question_b',
        type: 'text'
      }, 'wrapper');
      exampleIn.forEach(registerConditionalDisplay);
      $('#question_a').val('ONE').trigger('change');
      var display = $('#question_b').css('display');
      expect(display).to.equal('inline-block');

      $('#question_a').val('TWO').trigger('change');
      var display = $('#question_b').css('display');
      expect(display).to.equal('inline-block');

      $('#question_a').val('THREE').trigger('change');
      var display = $('#question_b').css('display');
      expect(display).to.equal('inline-block');      
    });

    it('[contains]: display:none before change', function() {
      createField('label', {
        id: 'question_label',
        class: 'question_a'
      }, 'wrapper');

      createField('input', {
        id: 'question_a',
        name: 'question_a',
        type: 'text',
        value: 'SOMETHING'
      }, 'question_label');

      createField('input', {
        id: 'question_b',
        class: 'question_b',
        type: 'text'
      }, 'wrapper');
      exampleContains.forEach(registerConditionalDisplay);
      var display = $('#question_b').css('display');
      expect(display).to.equal('none');
    });

    it('[contains]: display:none after false change', function() {
      createField('label', {
        id: 'question_label',
        class: 'question_a'
      }, 'wrapper');

      createField('input', {
        id: 'question_a',
        name: 'question_a',
        type: 'text',
        value: 'SOMETHING'
      }, 'question_label');

      createField('input', {
        id: 'question_b',
        class: 'question_b',
        type: 'text'
      }, 'wrapper');
      exampleContains.forEach(registerConditionalDisplay);
      $('#question_a').val('SOMETHING ELSE').trigger('change');
      var display = $('#question_b').css('display');
      expect(display).to.equal('none');
    });

    // it('[contains]: display:inline-block after change', function() {
    //   createField('label', {
    //     id: 'question_label',
    //     class: 'question_a'
    //   }, 'wrapper');

    //   createField('select', {
    //     id: 'question_a',
    //     name: 'question_a',
    //     type: 'text'
    //   }, 'question_label');
    //   createField('option', { value: 'A THING' }, 'question_a');
    //   createField('option', { value: 'SOMETHING' }, 'question_a');
    //   createField('option', { value: 'OTH', id: 'other-field' }, 'question_a');

    //   createField('input', {
    //     id: 'question_b',
    //     class: 'question_b',
    //     type: 'text'
    //   }, 'wrapper');
    //   console.log(document.body);
    //   exampleContains.forEach(registerConditionalDisplay);
    //   $('#question_a option').each(function() {
    //     if ($(this).val() === 'OTH') $(this).attr('selected', 'selected');
    //   });
    //   $('#question_a').trigger('change');
    //   var display = $('#question_b').css('display');
    //   expect(display).to.equal('inline-block');
    // });

    // it('[does_not_contain]: display:none before change', function() {
    //   createField('label', {
    //     id: 'question_label',
    //     class: 'question_a'
    //   }, 'wrapper');

    //   createField('input', {
    //     id: 'question_a',
    //     name: 'question_a',
    //     type: 'text',
    //     value: 'HELLO'
    //   }, 'question_label');

    //   createField('input', {
    //     id: 'question_b',
    //     class: 'question_b',
    //     type: 'text'
    //   }, 'wrapper');
    //   exampleDoesNotContain.forEach(registerConditionalDisplay);
    //   var display = $('#question_b').css('display');
    //   expect(display).to.equal('none');
    // });

    // it('[does_not_contain]: display:none after false change', function() {
    //   createField('label', {
    //     id: 'question_label',
    //     class: 'question_a'
    //   }, 'wrapper');

    //   createField('input', {
    //     id: 'question_a',
    //     name: 'question_a',
    //     type: 'text',
    //     value: 'NO'
    //   }, 'question_label');

    //   createField('input', {
    //     id: 'question_b',
    //     class: 'question_b',
    //     type: 'text'
    //   }, 'wrapper');
    //   exampleIn.forEach(registerConditionalDisplay);
    //   $('#question_a').val('FOUR').trigger('change');
    //   var display = $('#question_b').css('display');
    //   expect(display).to.equal('none');
    // });

    // it('[does_not_contain]: display:inline-block after change', function() {
    //   createField('label', {
    //     id: 'question_label',
    //     class: 'question_a'
    //   }, 'wrapper');

    //   createField('input', {
    //     id: 'question_a',
    //     name: 'question_a',
    //     type: 'text',
    //     value: 'NO'
    //   }, 'question_label');

    //   createField('input', {
    //     id: 'question_b',
    //     class: 'question_b',
    //     type: 'text'
    //   }, 'wrapper');
    //   exampleIn.forEach(registerConditionalDisplay);
    //   $('#question_a').val('ONE').trigger('change');
    //   var display = $('#question_b').css('display');
    //   expect(display).to.equal('inline-block');   
    // });
  });
});