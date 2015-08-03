/*
**  MAPS
**  If #service-map, grab info and make a map out of it
**
*/
window.Maps = window.Maps || {};
var Maps = function ( options ) {
  console.info('Maps initialized :)');

  if ($('#service-map').length) {
    makeTheMaps();
  }

  function makeTheMaps() {
    // temporary fake locations
    this.locations = [];
    this.keys = {
      accessToken: 'pk.eyJ1Ijoic3ZtYXR0aGV3cyIsImEiOiJVMUlUR0xrIn0.NweS_AttjswtN5wRuWCSNA',
      tileSet: 'svmatthews.lidab7g5'
    };
    this.id = 'service-map';

    _this = this;
    
    if (!$('.location').length) {
      var err = new Error('Maps: No locations specified. See https://github.com/codeforamerica/rva-screening-ui-prototypes/wiki/Maps');
      throw err;
    } else {
      $('.location').each(function(){
        var newLocation = {};
        newLocation.coordinates = [parseFloat($(this).attr('data-latitude')), parseFloat($(this).attr('data-longitude'))];
        newLocation.address = $(this).attr('data-address');
        _this.locations.push(newLocation);
      });

      L.mapbox.accessToken = this.keys.accessToken;
      this.mapObject = L.mapbox.map(this.id, this.keys.tileSet);
      this.markers = L.mapbox.featureLayer();
      this.locations.forEach(addMarker);
      function addMarker(location) {
        var content = location.address;

        var marker = L.marker(location.coordinates, {
          icon: L.mapbox.marker.icon({
            'marker-size': 'large',
            'marker-symbol': 'star',
            'marker-color': '#333'
          })
        }).bindPopup(content).addTo(_this.markers);
      }

      this.markers.addTo(this.mapObject);
      this.mapObject.fitBounds(this.markers.getBounds());

      // pans the map to the marker on location hover, and opens popup
      $('.location').on('mouseenter', function(e) {
        var elem = $(this);
        _this.markers.eachLayer(function(e){
          var ll = e.getLatLng();
          if(parseFloat(elem.attr('data-latitude')) === ll.lat) {
            e.togglePopup();
            _this.mapObject.panTo(ll);
          }
        });
      });
    }
  }
};