describe('> > > MAPS.JS', function() {

  var opts = {
    accessToken: 'pk.eyJ1Ijoic3ZtYXR0aGV3cyIsImEiOiJVMUlUR0xrIn0.NweS_AttjswtN5wRuWCSNA',
    tileSet: 'svmatthews.lidab7g5'
  };

  var badOpts = {
    tileSet: 'svmatthews.lidab7g5'
  };

  var optsNoTileSet = {
    accessToken: 'pk.eyJ1Ijoic3ZtYXR0aGV3cyIsImEiOiJVMUlUR0xrIn0.NweS_AttjswtN5wRuWCSNA'
  }

  var expectedLocations = [
    {
      address: '124 Radical Ave',
      coordinates: [
        37.547508,
        -77.447895
      ]
    }
  ];

  beforeEach(function() {
    loc = document.createElement('div');
    loc.className = 'location';
    loc.setAttribute('data-name', 'An Awesome Place');
    loc.setAttribute('data-address', '124 Radical Ave');
    loc.setAttribute('data-latitude', '37.547508');
    loc.setAttribute('data-longitude', '-77.447895');
    document.body.appendChild(loc);

    mapElem = document.createElement('div');
    mapElem.id = 'service-map';
    document.body.appendChild(mapElem);

    m = Maps // locally scoped Maps function for testing
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  describe('Initialization', function() {
    
    it('Throws error if no accessToken provided', function() {
      expect(function(){ m(badOpts); }).to.throw(Error);
    });

    it('Sets tileSet to default mapbox.streets if none provided', function() {
      var temp = new m(optsNoTileSet);
      expect(temp.tileSet).to.equal('mapbox.streets');
    });

    // TODO: allow user to pass map destination instead of forcing #service-map
    it('Throws error if no #service-map element on the page', function() {
      // remove the #service-map element
      var elem = document.getElementById('service-map');
      elem.parentElement.removeChild(elem);
      expect(function() { m(opts); }).to.throw(Error);
    });
  });

  describe('Locations & markers', function() {

    it('Throws error if no locations to add as markers to the map', function() {
      loc.parentElement.removeChild(loc);
      expect(function() { m(opts); }).to.throw(Error);
    });

    it('Latitude throws error if not a number', function() {
      loc.setAttribute('data-latitude', 'this is not a number');
      expect(function() { m(opts); }).to.throw(Error);
    });

    it('Longitude throws error if not a number', function() {
      loc.setAttribute('data-longitude', 'this is not a number');
      expect(function() { m(opts); }).to.throw(Error);
    });

    it('If location element is missing address, don\'t add popup', function() {
      loc.setAttribute('data-address', ''); // remove address
      var map = new m(opts);
      var popupContent = '';
      for (key in map.markers._layers) {
        var tempMarker = map.markers._layers[key];
        var info = tempMarker.getPopup();
        // if the function doesn't exist, it doesn't have a popup
        expect(typeof info).to.eq('undefined');
      }
    });

    it('returns proper location array with Maps.parseLocation', function() {
      var map = new m(opts);
      expect(map.locations).to.deep.eq(expectedLocations);
    });

    // can we think of a better way to ensure it's properly turned into a leaflet marker object?
    // Currently it just assumes the markers object has a _layers key
    it('Locations are converted to markers and have the same length', function() {
      var map = new m(opts);
      var locationCount = document.getElementsByClassName('location').length;
      expect(Object.keys(map.markers._layers).length).to.equal(locationCount);
    });

    // test user hover on location elements

    // ensure markers are added to map object

    // ensure map object has fit to the bounds
    // it('fits the markers to the bounds of the map element', function() {
    //   var map = new m(opts);
    //   expect(map.markers.getBounds()).to.deep.equal(map.mapObject.getCenter());
    // });
  });


});