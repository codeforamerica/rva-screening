describe('Vendor Libraries', function() {

  describe('They exist', function() {
    it('jQuery', function() {
      expect(typeof jQuery).to.equal('function');
    });

    it('mapbox.js', function() {
      expect(typeof L).to.equal('object');
    });

    it('Fuse.js', function() {
      expect(typeof Fuse).to.equal('function');
    });
  });
});