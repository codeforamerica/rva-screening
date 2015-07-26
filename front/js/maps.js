/*
**  MAPS
**  If #service-map, grab info and make a map out of it
**
*/
window.Maps = window.Maps || {};
var Maps = function ( options ) {
  console.info('Maps initialized :)');
  if ($('#service-map').length) {

    // temporary fake locations
    this.locations = [];
    this.keys = {
      accessToken: 'pk.eyJ1Ijoic3ZtYXR0aGV3cyIsImEiOiJVMUlUR0xrIn0.NweS_AttjswtN5wRuWCSNA',
      tileSet: 'svmatthews.lidab7g5'
    };
    this.id = 'service-map';

    var _this = this;
    
    if (!$('.location').length) {
      console.error('Maps: No locations specified. See https://github.com/codeforamerica/rva-screening-ui-prototypes/wiki/Maps');
      return;
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
    }
  }
};