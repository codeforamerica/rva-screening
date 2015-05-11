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
}