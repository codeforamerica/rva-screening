$(document).ready(function(){
  /*
  **  PATIENT DETAILS / UNIQUE QUESTIONS FILTERS
  **  Shows/hides service-specific questions on the page based on
  **  checkbox values
  **
  */
  var serviceFilters = $('.patient_details_filter .field_checkbox input[type="checkbox"]');
  serviceFilters.on('change', function(e) {
    serviceFilterChange($(this));
  });


  /*
  **  PATIENT LISTS - index.html
  **  Shows/hides specific individuals if they match a filter
  **  criteria listed on the left-hand side of the page
  **
  */
  $('.filter').on('click', function(){
    listFilterClick($(this));
  });
});

function listFilterClick($this) {
  $('.filter').removeClass('filter_active');
  $this.addClass('filter_active');

  $('.list_filter').removeClass('list_filter_active');
  var id = $this.attr('data-list');
  $('#list-'+id).addClass('list_filter_active');
}

function serviceFilterChange($this) {
  var select = $('.'+$this.attr('name'));
  if ($this.is(':checked')) {
    select.show();
  } else {
    select.hide();
  }
}