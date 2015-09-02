describe('Multiform actions', function() {
  beforeEach(function() {
    createMultiform();
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

});