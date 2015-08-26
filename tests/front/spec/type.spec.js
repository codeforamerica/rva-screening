describe('Type', function() {

  describe('Exist as functions', function() {
    it('AppController', function() {
      expect(typeof AppController).to.equal('function');
    });

    it('Menu', function() {
      expect(typeof Menu).to.equal('function');
    });

    it('Maps', function() {
      expect(typeof Maps).to.equal('function');
    });

    it('Search', function() {
      expect(typeof Search).to.equal('function');
    }); 

    it('Validator', function() {
      expect(typeof Validator).to.equal('function');
    });

    it('Conditional Display', function() {
      expect(typeof registerConditionalDisplay).to.equal('function');
    });
  });

  describe('Exist as objects', function() {
    // test for needed objects?
  });

});