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

    var valueFName = $('#field_search_patient_first_name').val();
    var valueLName = $('#field_search_patient_last_name').val();
    var valueDob = $('#field_search_patient_dob').val();
    var valueSsn = $('#field_search_patient_ssn').val();
    var res = JSON.search( S.data, '//*[contains(fname, "'+valueFName+'") and contains(lname, "'+valueLName+'") and contains(dob, "'+valueDob+'") and contains(ssn, "'+valueSsn+'")]' );
    var results = translateResults(res, valueFName + ' ' + valueLName);

    if (res.length > S.data.total) {
      var html = "";
    } else if (!res.length) {
      var html = templates.render('noresults', results);
      // var html = Defiant.render('search_noresults', results);
    } else {
      var html = templates.render('list', results);
      // var html = Defiant.render('search_results_list', results);
    }
    
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

var templates = {
  render: function(fn, array) {
    var html = this[fn](array);
    return html;
  },
  list: function(data) {
    var elem = document.createElement('ul');
    elem.className = 'list list_table list_search';
    for (var p = 0; p < data.patients.length; p++) {
      var patient = data.patients[p];
      var li = document.createElement('li');
      li.className = 'list_row';
      
      var anchor = document.createElement('a');
      anchor.href = patient.url;
      anchor.innerHTML += '<div class="block_3 patient_search_result_item">' + patient.fname + '</div>';
      anchor.innerHTML += '<div class="block_3 patient_search_result_item">' + patient.lname + '</div>';
      anchor.innerHTML += '<div class="block_3 patient_search_result_item">' + patient.dob + '</div>';
      anchor.innerHTML += '<div class="block_3 patient_search_result_item">' + patient.ssn + '</div>';

      li.appendChild(anchor);
      elem.appendChild(li);
    }


    var newPatient = document.createElement('li');
    newPatient.href = newPatientUrl;
    newPatient.innerHTML = '<div class="block_12"><button class="button button_blue button_large patient_search_button" type="submit">Add <strong>' + data.none[0].name + '</strong> as a new patient</button></div>';
    elem.appendChild(newPatient);

    return elem;
  },
  noresults: function(data) {
    var elem = document.createElement('ul');
    elem.className = 'list list_table list_search';
    
    var li = document.createElement('li');
    li.className = 'list_row'
    elem.innerHTML = '<div class="block_12 patient_search_result_item patient_search_noresults"><i class="fa fa-exclamation-circle"></i> No patients matched <strong>' + data.none[0].name + '</strong></div>';    
    elem.appendChild(li);

    var newPatient = document.createElement('li');
    newPatient.href = newPatientUrl;
    newPatient.innerHTML = '<div class="block_12"><button class="button button_blue button_large patient_search_button" type="submit">Add <strong>' + data.none[0].name + '</strong> as a new patient</button></div>';
    elem.appendChild(newPatient);
  
    return elem;
  }
};