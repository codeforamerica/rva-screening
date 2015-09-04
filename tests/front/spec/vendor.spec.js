describe('Vendor Libraries', function() {

  describe('They exist', function() {
    it('jQuery', function() {
      expect(typeof jQuery).to.equal('function');
    });

    it('mapbox.js', function() {
      expect(typeof L).to.equal('object');
    });

    it('Defiant.js', function() {
      expect(typeof Defiant).to.equal('object');
    });

    it('list.js', function() {
      expect(typeof List).to.equal('function');
    }); 
  });
});