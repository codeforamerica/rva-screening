window.App = window.App || {};

var inputClearingFunctions = [
  ['input', function(){ $(this).val(''); }],
  ['textarea', function(){ $(this).html(''); }],
  ['select', function(){ $(this).children().each(function(){
    if( $(this).hasClass('default-choice')){ this.selected = true;
    } else { this.selected = false; }
  }); }]
];

var AppController = function ( options ) {
  console.info('App initialized :)');
  this.options = options || {};
  addEventListeners();
  function addEventListeners() {
    /*
    **  EXPANDER CLICK
    **  This toggles the expander element and animates.
    **
    */
    $('.expander-title').on('click', function(){
      $(this).parent().toggleClass('open');
      $(this).next('.expander-content').slideToggle(300);
    });

    /*
    **  ADD FORM ITEM CLICK
    **  This adds new empty forms for many-to one items
    **  .form-list contains both .add-form-list-item and .form-list-item
    *   .form-list-item is the div to be added
    */
    $('.multiform_control_edit').on('click', function(e){
      e.preventDefault();
      var entry = $(this).parent().parent();
      var entryForm = entry.find('.multiform_content_fields');
      var entryRead = entry.find('.multiform_content_readonly');

      if (entry.hasClass('form_multiform_read')) {
        entry.removeClass('form_multiform_read');
        entry.addClass('form_multiform_edit');
      }

      return;
    });

    $('.multiform_control_remove').on('click', function(e){
      e.preventDefault();
      var entry = $(this).parent().parent();
      var entryForm = entry.find('.multiform_content_fields');
      entryForm.find('.field_input').each(function(){
        $(this).attr('value', '');
        if ($(this).attr('type') == 'date') {
          $(this).attr('value', 'mm/dd/yyyy');
        }
      });
      entry.hide();
      // entry.remove(); // removes from DOM, not from db until page save
      return;
    });

    $('.multiform_control_add').on('click', function(e){
      e.preventDefault();
      var id = $(this).attr('data-clone-id');
      var clone = $('#'+id).clone();
      $('#'+id).after(clone);
      // console.log(id, clone);
      return;
    });

  }

  /*
  **  SEARCH FIELD CHECK
  **  If #patient-search exists, initialize the search
  **
  */
  if ($('#patient-search').length) {
    this.search = {};
    this.initSearch('patient-search', 
        { valueNames: ['patient-name', 'patient-dob'] });
  }


  // If we're on the print page, hide everything that shouldn't print
  if (window.location.pathname.indexOf('/patient_print') > -1) {
    convertForPrint();
  }

};


/*
**  SEARCH INITIALIZATION
**  @param(id) - the element ID of the list you're making searchable
**  @param(options) - options you can pass through, currently just an array
**    of valueNames for the classes in your list items you want to make
**    searchable.
**
*/
AppController.prototype.initSearch = function ( id, options ) {
  this.search.id = id;
  this.search.options = options;
  this.search.list = new List(id, options);
};


function convertForPrint() {
  $('#patient_details_form').find(':input').not('.hidden-input').not('.hidden').replaceWith(function(){
    return '<span>'+this.value+'</span>'
  });
  $('.expander').replaceWith(function(){
    return $(this).children()
  });
  $('.expander-title').hide();
  $('table').not('#phone_number_table').find('th:last-child, td:last-child').hide();
}


/*
**  REQUEST BUTTON CLICK / UPDATE
**  Updates the className of the patient-list-item and changes
**  the text within the button.
**
*/
function sharePatientInfo( btn, patient_id, app_user_id, service_id ) {
  $.post('/add_referral', {
    patient_id: patient_id,
    app_user_id: app_user_id,
    service_id: service_id
  }).done(function() {
    $(btn).addClass('shared');
    $(btn).text('Referral sent!');
  });
}


