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
    $('.add-form-list-item').on('click', function(){
      var formClone = $(
          $(this).siblings('.form-list-item')[0]
        ).clone();
      inputClearingFunctions.forEach(function(selectorFunctionPair){
        console.log("selectorFunctionPair", selectorFunctionPair);
        var selector = selectorFunctionPair[0];
        var fn = selectorFunctionPair[1];
        formClone.find(selector).each(fn);
      });
      formClone.insertBefore(this).removeClass('hidden');
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

  /*
  **  PATIENT DETAILS / UNIQUE QUESTIONS FILTERS
  **  Shows/hides service-specific questions on the page based on
  **  checkbox values
  **
  **  TODO: move into filters.js
  **
  */
  var serviceFilters = $('.patient_details_filter .field_checkbox input[type="checkbox"]');
  var allUniqueQuestions = $('.q_unique');
  serviceFilters.on('change', function(e) {
    var checked = [];

    // get all checked filters
    serviceFilters.each(function(){
      if($(this).is(':checked')) {
        checked.push($(this).attr('name'));
      }
    });

    // hide all question fields
    allUniqueQuestions.hide();

    // now bring them back if they match the checked
    // boxes on the filters
    allUniqueQuestions.each(function(){
      var q = $(this);
      for (var c = 0; c < checked.length; c++) {
        if (q.hasClass(checked[c])) {
          q.show();
        }
      }
    });

  });

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


function addNewInputRow($table, $input_row) {
  $new_row = $input_row.clone();
  $new_row.each(function() {
    $(this).attr('id', '');
    var input = $(this).find(':input');
    input.val('');
  });
  $table.append($new_row);
  return;
}

function hideRow() {
  $(event.target).parent().siblings().each(
    function() {
      $(this).find(".hidden-input").attr('value', '');
      $(this).find("input[type='date'].hidden-input").attr('value', 'mm/dd/yyyy');
    }
  );
  $(event.target).parent().parent().hide();
}

function showHiddenFields() {
  $(event.target).parent().siblings().each(
    function() {
      $(this).find(".hidden-input").show();
      $(this).find(".read-only").hide();
    }
  );
}

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
    $(btn).text('referral sent');
  });
}


