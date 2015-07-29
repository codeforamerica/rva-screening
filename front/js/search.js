/*
**  SEARCH
**  If #search exists, load tempSearchData as a large JSON for Defiant.js
**  `tempSearchData` is currently being created in index.html as a global variable
**
*/
window.Search = window.Search || {};
var Search = function ( options ) {
  console.info('Search initialized :)')
  this.options = options;
  $('.field_input_search').on('keyup', function(e){
    // console.log($(this).val());
    var valueName = $('#field_search_patient_name').val();
    var valueDob = $('#field_search_patient_dob').val();
    var valueSsn = $('#field_search_patient_ssn').val();
    var res = JSON.search( tempSearchData, '//*[contains(name, "'+valueName+'") or contains(dob, "'+valueDob+'") or contains(ssn, "'+valueSsn+'")]' );
    var results = {
      patients: res,
      none: [
        {
          name: valueName
        }
      ]
    };
    console.log(results);
    if (res.length > tempSearchData.total) {
      var html = "";
    } else if (!res.length) {
      var html = Defiant.render('search_noresults', results);
    } else {
      var html = Defiant.render('search_results_list', results);
    }
    $('#search_results').html(html);
  });
}