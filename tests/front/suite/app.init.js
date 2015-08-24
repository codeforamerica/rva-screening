describe('TEST', function() {
  
  var areWeTestingYet = false;

  function startTesting(a) {
    return a = !a;
  }

  describe('The test that tests if we are testing', function () {
    it('we are testing!', function () {
      expect(startTesting(areWeTestingYet)).to.eq(true);
    });
  });
});