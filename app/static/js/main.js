window.App = window.App || {};

var AppController = function ( options ) {
  console.info('APP INITIALIZED :)');
  this.options = options || {};
  this.hiphip = 'hooray!';
  console.log(this);

  if ($('#patient-search').length) {
    this.search = {};
    this.initSearch('patient-search', { valueNames: ['patient-name', 'patient-dob'] });
  }
};

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

function requestPatientButtonClick( btn ) {
  $(btn).parent().parent().addClass('requested');
  $(btn).text('request sent');
}