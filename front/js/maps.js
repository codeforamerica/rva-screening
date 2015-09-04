/*
**  MAPS
**  If #service-map, grab info and make a map out of it
**
*/
window.Maps = window.Maps || {};
var Maps = function ( options ) {

  this.options = options;

  if (!options.accessToken) {
    var err = new Error('No accessToken provided');
    throw err;
  }
  this.accessToken = options.accessToken;
  this.tileSet = !options.tileSet ? 'mapbox.streets' : options.tileSet;
  this.locations = [];
  this.id = 'service-map'; // TODO: decouple this from the Maps() function
  this.locationElemes

  if (!$('#service-map').length) {
    var err = new Error('There is no #service-map id to attach the map to');
    throw err;
  } else {
    this.init();
  }
};

Maps.prototype.init = function() {

  var _this = this;
    
  if (!$('.location').length) {
    var err = new Error('Maps: No locations specified. See https://github.com/codeforamerica/rva-screening-ui-prototypes/wiki/Maps');
    throw err;
  } else {
    $('.location').each(function(){
      var loc = _this.parseLocation($(this));
      _this.locations.push(loc);
    });

    L.mapbox.accessToken = this.accessToken;
    this.mapObject = L.mapbox.map(this.id, this.tileSet);
    this.markers = L.mapbox.featureLayer();
    this.locations.forEach(function(location){
      var m = _this.createMarker(location);
      m.addTo(_this.markers)
    });
    this.markers.addTo(this.mapObject);
    this.mapObject.fitBounds(this.markers.getBounds());

    // pans the map to the marker on location hover, and opens popup
    $('.location').on('mouseenter', function(e) {
      _this.centerMap($(this));
    });
  }
};

// takes a location jQuery element and centers the map on it
Maps.prototype.centerMap = function($elem) {
  var _this = this;
  this.markers.eachLayer(function(e){
    var ll = e.getLatLng();
    if(parseFloat($elem.attr('data-latitude')) === ll.lat) {
      e.togglePopup();
      _this.mapObject.panTo(ll);
    }
  });
};

Maps.prototype.parseLocation = function($elem) {
  var newLocation = {};
  var lat = parseFloat($elem.attr('data-latitude'));
  var lon = parseFloat($elem.attr('data-longitude'));
  if (isNaN(lat)) {
    var err = new Error('Latitude is not a proper number. Please make sure it exists.');
    throw err;
  }
  if (isNaN(lon)) {
    var err = new Error('Longitude is not a proper number. Please make sure it exists.');
    throw err;
  }
  newLocation.coordinates = [lat, lon];
  newLocation.address = $elem.attr('data-address');
  return newLocation;
}

Maps.prototype.createMarker = function(location) {
  var content = location.address;
  var marker = L.marker(location.coordinates, {
    icon: L.mapbox.marker.icon({
      'marker-size': 'large',
      'marker-symbol': 'star',
      'marker-color': '#333'
    })
  });
  if (content.length) {
    marker.bindPopup(content);
  }
  return marker;
}