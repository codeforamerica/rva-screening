describe('Multiform actions', function() {
  
  beforeEach(function() {
    createMultiform(); // helpers.js
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('multiform.add() clones properly', function() {
    multiform.add('data_clone_test');
    // expect two instances of .form_multiform to be three after multiform.add()
    expect(document.getElementsByClassName('form_multiform').length).to.equal(3);
  });

  it('multiform.edit() switches classes properly', function() {
    multiform.edit($('#test_edit_button'));
    expect($('#test_multiform').hasClass('form_multiform_read')).to.equal(false);
  });

  // tests to remove field and removes input values
  it('multiform.remove() hides multiform', function() {
    multiform.remove($('#test_remove_button'));
    expect($('#test_multiform').css('display')).to.equal('none');
  });

  it('multiform.remove() removes input values', function() {
    multiform.remove($('#test_remove_button'));
    var i = $('#something-0').val();
    expect(i).to.equal('');
  });

  it('multiform.remove() resets date values', function() {
    // change something-0 to a date field first
    $('#something-0').attr({'type': 'date', 'value': '1989-02-09'});
    multiform.remove($('#test_remove_button'));
    var i = $('#something-0').val();
    expect(i).to.equal('mm/dd/yyyy');
  });

});