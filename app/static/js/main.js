window.App = window.App || {};

var AppController = function ( options ) {
  console.info('APP INITIALIZED :)');
  this.options = options || {};
  this.waka = 'flaka';
  this.hiphip = 'hooray!';
  console.log(this);


  addEventListeners();
  function addEventListeners() {

    // expander sections
    $('.expander-title').on('click', function(){
      $(this).parent().toggleClass('open');
      $(this).next('.expander-content').slideToggle(300);
    });
  }
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