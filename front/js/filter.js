$(document).ready(function(){
  /*
  **  PATIENT DETAILS / UNIQUE QUESTIONS FILTERS
  **  Shows/hides service-specific questions on the page based on
  **  checkbox values
  **
  */
  var serviceFilters = $('.patient_details_filter .field_checkbox input[type="checkbox"]');
  // var allUniqueQuestions = $('.q_unique');
  serviceFilters.on('change', function(e) {
    // var checked = [];

    // // get all checked filters
    // serviceFilters.each(function(){
    //   if($(this).is(':checked')) {
    //     checked.push($(this).attr('name'));
    //   }
    // });

    // // hide all question fields
    // allUniqueQuestions.hide();

    // // now bring them back if they match the checked
    // // boxes on the filters
    // allUniqueQuestions.each(function(){
    //   var q = $(this);
    //   for (var c = 0; c < checked.length; c++) {
    //     if (q.hasClass(checked[c])) {
    //       q.show();
    //     }
    //   }
    // });
    var select = $('.'+$(this).attr('name'));
    if ($(this).is(':checked')) {
      select.show();
    } else {
      select.hide();
    }
  });


  /*
  **  PATIENT LISTS - index.html
  **  Shows/hides specific individuals if they match a filter
  **  criteria listed on the left-hand side of the page
  **
  */
  $('.filter').on('click', function(){
    $('.filter').removeClass('filter_active');
    $(this).addClass('filter_active');

    $('.list_filter').removeClass('list_filter_active');
    var id = $(this).attr('data-list');
    $('#list-'+id).addClass('list_filter_active');
  });
});