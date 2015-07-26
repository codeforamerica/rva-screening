/*
**  SEARCH
**  If #search exists, load patients as a large JSON for Defiant.js
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
    var res = JSON.search( patients, '//*[contains(name, "'+valueName+'") or contains(dob, "'+valueDob+'") or contains(ssn, "'+valueSsn+'")]' );
    console.log(res.length, patients.total);
    var results = {
      patients: res,
      none: [
        {
          name: valueName
        }
      ]
    };
    if (res.length > patients.total) {
      var html = "";
    } else if (!res.length) {
      var html = Defiant.render('search_noresults', results);
    } else {
      var html = Defiant.render('search_results_list', results);
    }
    $('#search_results').html(html);
  });

  $('.filter').on('click', function(){
    $('.filter').removeClass('filter_active');
    $(this).addClass('filter_active');

    $('.list_filter').removeClass('list_filter_active');
    var id = $(this).attr('data-list');
    $('#list-'+id).addClass('list_filter_active');
  });
}

/*
**  PATIENT DATA USED FOR SEARCH
**
*/
window.patients = {
  total: 10,
  list: [
    {
      name: 'Sam Matthews',
      dob: '02/09/1989',
      ssn: '469-23-9973'
    },
    {
      name: 'Sarah Johnson',
      dob: '02/09/1989',
      ssn: '469-23-9973'
    },
    {
      name: 'Cotton Awesome',
      dob: '02/09/1989',
      ssn: '469-23-9973'
    },
    {
      name: 'Super Duper',
      dob: '02/09/1989',
      ssn: '222-33-4444'
    },
    {
      name: 'John Matthews',
      dob: '02/09/1989',
      ssn: '469-23-9973'
    },
    {
      name: 'Sam Johnson',
      dob: '02/09/1989',
      ssn: '469-23-9973'
    }
  ]
};