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
  // console.info('App initialized :)');
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
    $('.multiform_control_edit').on('click', function(e) {
      e.preventDefault();
      multiform.edit($(this));
      return;
    });
    $('.multiform_control_remove').on('click', function(e) {
      e.preventDefault();
      multiform.remove($(this));
      return;
    });
    $('.multiform_control_add').on('click', function(e) {
      e.preventDefault();
      multiform.add($(this).attr('data-clone-id'));
      return;
    });
    $('.multiform_control_check').on('click', function(e) {
      e.preventDefault();
      multiform.check($(this));
      return;
    });

    // sticky sidebar for patient nav
    if ($('#stickyNav').length) {
      var $nav = $('#stickyNav');
      var navFromTop = $nav.offset().top;
      $(window).scroll(function(){
        var fromTop = $(window).scrollTop();
        if (fromTop > navFromTop) {
          if (!$nav.hasClass('sticky')) {
            $nav.css('width', $nav.width());
            $nav.addClass('sticky');
          }
        } else {
          $nav.css('width', 'auto');
          $nav.removeClass('sticky');
        }
      });  
    }
    
  }

  // If we're on the print page, hide everything that shouldn't print
  if (window.location.pathname.indexOf('/patient_print') > -1) {
    convertForPrint();
  }

};

var multiform = {
  add: function(id) {
    console.log(id);
    var clone = $('#'+id).clone();
    var elem_id = clone.find(":input")[0].id;
    var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
    clone.attr('data-id', elem_num);
    clone.find(":input").each(function() {
      var new_elem_id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
      $(this).attr('name', new_elem_id).attr('id', new_elem_id).val('').removeAttr("checked");
    });
    clone.removeClass('form_multiform_copy');
    clone.addClass('form_multiform_new');
    $('#'+id).after(clone);
  },
  remove: function($button) {
    var entry = $button.parent().parent();
    var entryForm = entry.find('.multiform_content_fields');
    entryForm.find('.field_input').each(function(){
      $(this).trigger('change').attr('value', '');
      if ($(this).attr('type') == 'date') {
        $(this).trigger('change').attr('value', 'mm/dd/yyyy');
      }
      if ($(this).is('select')) {
        $(this).trigger('change').val('');
      }
    });
    entry.hide();
  },
  edit: function($button) {
    var entry = $button.parent().parent();
    if (entry.hasClass('form_multiform_read')) {
      entry.removeClass('form_multiform_read');
      entry.addClass('form_multiform_edit');
    }
  },
  check: function($button) {
    var entry = $button.parent().parent();
    if (entry.hasClass('form_multiform_edit')) {
      entry.removeClass('form_multiform_edit');
      entry.addClass('form_multiform_read');
    }
  }
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
function sharePatientInfo( elem, patient_id, app_user_id, service_id, notes_id ) {
  var referralNotes = $('#'+notes_id).val();
  $(elem).html('Sending <i class="fa fa-spinner loading"></i>');
  $.post('/add_referral', {
    patient_id: patient_id,
    app_user_id: app_user_id,
    service_id: service_id,
    notes: referralNotes
  }).done(function() {
    $(elem).removeClass('button_green').addClass('button_blue');
    $(elem).parent().html('<a class="button button_blue pull-right" href="/patient_overview/' + patient_id + '">Sent! View referral</a>');
    $(elem).remove();
  });
}