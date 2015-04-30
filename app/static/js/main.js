window.App = window.App || {};

var AppController = function ( options ) {
  this.options = options || {};
  this.waka = 'flaka';
  console.info('APP INITIALIZED :)');
  console.log(this);
};