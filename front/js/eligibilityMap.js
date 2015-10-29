/*
**  MAPS
**  If #service-map, grab info and make a map out of it
**
*/
window.EligiblityMap = window.EligibilityMap || {};
var EligibilityMap = function ( options ) {

  this.options = options;

  if (!options.accessToken) {
    var err = new Error('No accessToken provided');
    throw err;
  }
  this.accessToken = options.accessToken;
  this.tileSet = !options.tileSet ? 'mapbox.streets' : options.tileSet;
  if (options.data === null) {
    var err = new Error('Eligibility data is null!');
    throw err;
  }
  this.data = options.data;

  if (!options.elem) {
    var err = new Error('No map container provided!');
    throw err;
  }
  this.id = options.elem;

  this.init();
};

EligibilityMap.prototype.init = function() {

  var _this = this;
  console.log(_this);

  L.mapbox.accessToken = this.accessToken;
  this.map = L.mapbox.map(this.id, this.tileSet);
  this.markers = L.mapbox.featureLayer();

  $(this.data).each(function() {

    var ELIGIBILITY = this.calculatedEligibility;
    var URL = this.url;
    var NAME = this.service

    $(this.locations).each(function() {

      var marker = L.marker(this.coordinates, {
        icon: L.mapbox.marker.icon({
          'marker-size': 'large',
          'marker-symbol': ( ELIGIBILITY === 'true' ? 'star' : 'roadblock'),
          'marker-color': ( ELIGIBILITY === 'true' ? '#2ecc40' : '#f7aa9e' )
        })
      });

      var content = '<strong>' + NAME + ': ' + this.name + '</strong><br>' + this.address + '<br><a href="' + URL + '">View service profile</a>';

      marker.bindPopup(content);

      marker.addTo(_this.markers);

    });

  });

  this.markers.addTo(this.map);

  this.map.fitBounds(this.markers.getBounds());
  this.map.scrollWheelZoom.disable();

  $('#expandServiceEligibilityMap').on('click', function(e) {
    e.preventDefault();
    if ($(this).attr('data-expanded') === 'false') {
      $('#service-eligibility-map').addClass('expanded');
      $(this).attr('data-expanded', 'true')
        .text('Less map')
    } else {
      $('#service-eligibility-map').removeClass('expanded');
      $(this).attr('data-expanded', 'false')
        .text('Full map');
    }
    
    _this.map.invalidateSize()
    _this.map.fitBounds(_this.markers.getBounds());
    return false;
  });
  
};