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
    elem.className = 'list list_table';
    for (var p = 0; p < data.patients.length; p++) {
      var patient = data.patients[p];
      var li = document.createElement('li');
      li.className = 'list_row';
      
      var anchor = document.createElement('a');
      anchor.href = patient.url;
      anchor.innerHTML += '<span class="list_row_item list_row_name">' + patient.fname + ' ' + patient.lname + '</span>';
      anchor.innerHTML += '<span class="list_row_item list_row_dob">' + patient.dob + '</span>';
      anchor.innerHTML += '<span class="list_row_item list_row_edits">' + patient.created + '</span>';

      li.appendChild(anchor);
      elem.appendChild(li);
    }
    var newPatient = document.createElement('a');
    newPatient.href = newPatientUrl;
    newPatient.innerHTML = '<i class="fa fa-plus"></i> Not the right <strong>' + data.none[0].name + '</strong>? Add them as a new patient.';

    var addNew = document.createElement('li');
    addNew.className = 'list_row list_row_addnew';
    addNew.appendChild(newPatient);
    elem.appendChild(addNew);

    return elem;
  },
  noresults: function(data) {
    var elem = document.createElement('div');
    elem.className = 'no_results';
    elem.innerHTML = '<p><i class="fa fa-exclamation-circle"></i> No patients matched <strong>' + data.none[0].name + '</strong></p>';
    
    var newPatient = document.createElement('button');
    newPatient.className = 'button button_blue button_fat button_add';
    newPatient.setAttribute('type', 'submit');
    // newPatient.href = newPatientUrl || '/new_patient';
    newPatient.innerHTML = 'Create a new patient record with ' + data.none[0].name;
    
    elem.appendChild(newPatient);
    return elem;
  }
};