describe('main.js', function() {

  var app;
  var opts = { foo: 'bar' };

  beforeEach(function() {
    app = new AppController(opts);
  });

  describe('Initialization', function() {
    it('AppController is initialized with options', function() {
      expect(app.options).to.equal(opts);
    });
  });

});