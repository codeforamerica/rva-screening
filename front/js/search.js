/*
**  SEARCH
**  If #search exists, load tempSearchData as a large JSON for Defiant.js
**  `tempSearchData` is currently being created in index.html as a global variable
**
**  TODO: turn search into a pub/sub similar to validation.js
*/
window.Search = window.Search || {};
var Search = function ( options ) {

  if (!options) {
    var err = new Error('No search options provided. Please include elementClass & searchData');
    throw err;
  }

  this.options = options;
  this.elementClass = options.elementClass;
  this.data = options.searchData;
  var S = this;

  // if there is no elementClass to work with, throw an error
  if (!options.elementClass) {
    var err = new Error('There is no class to initialize search on');
    throw err;
  }

  // ensure search data exist
  if (!this.data) {
    var err = new Error('Cannot find the searchData option. Please include it as an option when initializing search.');
    throw err;
  }

  // check search data length
  if (this.data.total != this.data.list.length) {
    var err = new Error('Search Data: It looks like the specified length vs the actual length are different.');
    throw err;
  }

  $(this.elementClass).on('keyup', function(e){

    var valueName = $('#field_search_patient_name').val();
    var valueDob = $('#field_search_patient_dob').val();
    var valueSsn = $('#field_search_patient_ssn').val();
    var res = JSON.search( S.data, '//*[contains(name, "'+valueName+'") or contains(dob, "'+valueDob+'") or contains(ssn, "'+valueSsn+'")]' );
    var results = translateResults(res, valueName);

    if (res.length > S.data.total) {
      var html = "";
    } else if (!res.length) {
      var html = Defiant.render('search_noresults', results);
    } else {
      var html = Defiant.render('search_results_list', results);
    }
    console.log(html);
    $('#search_results').html(html);
  });
}

function translateResults(r, n) {
  return { 
    patients: r,
    none:[
      { 
        name: n 
      }
    ]
  };
}