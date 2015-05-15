window.App = window.App || {};

var AppController = function ( options ) {
  console.info('APP INITIALIZED :)');
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
  }

  /*
  **  SEARCH FIELD CHECK
  **  If #patient-search exists, initialize the search
  **
  */
  if ($('#patient-search').length) {
    this.search = {};
    this.initSearch('patient-search', { valueNames: ['patient-name', 'patient-dob'] });
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

function addNewInputRow($table, $input_row) {
	current_length = $input_row.length;
	$new_row = $input_row.clone();
	$new_row.each(function() {
		this.id += current_length;
		// $(this).find("input").each(function() {
		// 	this.name +=current_length;
		// })
	})
	$table.append($new_row);
	return;
}

function showHiddenFields() {
	$(event.target).parent().siblings().each(
		function() {
			$(this).find(".hidden-input").show().prop('disabled', false);
			$(this).find(".read-only").hide().prop('disabled', true);
		}
	);
}


/*
**  REQUEST BUTTON CLICK / UPDATE
**  Updates the className of the patient-list-item and changes
**  the text within the button.
**
*/
function sharePatientInfo( btn ) {
  $(btn).addClass('shared');
  $(btn).text('information sent');
}